import os
from pathlib import Path
import pandas as pd
import importlib.resources as pkg_resources
from tqdm import tqdm
import requests
from time import sleep


def get_microrganism_list(df: pd.DataFrame) -> list:
    """
    Get a list of microorganisms from a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with microbiome dara from which to extract the microorganisms.

    Returns
    -------
    species : list
        List of microorganisms
    """
    data = df.copy()
    data = data.drop(index="#CLASS")
    data = data.astype(float)
    data["org_sum"] = data.sum(axis=1)

    sum_df = data["org_sum"]
    sum_df = sum_df.reset_index(drop=False)

    duplicates = sum_df.duplicated(subset=sum_df.columns.difference(['org_sum']), keep=False)

    # Sum the 'org_sum' values for the duplicate rows
    sum_df.loc[duplicates, 'org_sum'] = (
        sum_df.groupby(sum_df.columns.difference(['org_sum']).tolist())['org_sum'].transform('sum'))

    # Drop the duplicate rows, keeping the first occurrence
    sum_df = sum_df.drop_duplicates(subset=sum_df.columns.difference(['org_sum']), keep='first')

    # Reset the index
    sum_df = sum_df.reset_index(drop=True)

    split_data = sum_df['#NAME'].str.split(';', expand=True)
    split_data = split_data.rename(columns={0: '#k', 1: '#p', 2: '#c', 3: '#o', 4: '#f', 5: '#g', 6: '#s'})
    split_data = split_data.apply(lambda x: x.str.strip())
    sum_df.drop(columns=["#NAME"], inplace=True)
    sum_df_splitted = pd.concat([split_data, sum_df], axis=1)

    def get_first_non_none_value(row):
        for col in ['#s', '#g']:
            if pd.notna(row[col]):
                return row[col]
        return None

    # Apply the function to each row in the DataFrame
    sum_df_splitted['desired_value'] = sum_df_splitted.apply(get_first_non_none_value, axis=1)

    # Replace underscores with spaces, check for " sp" and append to species list
    species = []
    for elem in sum_df_splitted['desired_value'].values:
        if elem is not None:
            elem = elem.replace("_", " ")
            if elem.endswith(" sp"):
                elem += "."
            species.append(elem)

    print(f'\nNumber of microorganisms present in this data: {len(species)}')
    print(f'Number of unique microorganisms present in this data: {len(set(species))}')

    return species


def get_taxid(species: list) -> dict:
    """
    Get a list of taxids from a list of species.

    Parameters
    ----------
    species : list
        List of species for which to get the taxids.

    Returns
    -------
    tax_ids : list
        List of taxids
    """

    taxonomy_path = pkg_resources.files("biomeanalyzer") / "data" / "taxonomy.tsv"
    taxonomy_path = str(taxonomy_path)
    tax_df = pd.read_csv(taxonomy_path, sep='\t', low_memory=False)

    found_species = tax_df[tax_df['name'].isin(species)]['name'].tolist()
    print(f"\nNumber of species with Tax ID found: {len(found_species)}")

    not_found_species = set(species) - set(found_species)
    print(f"Number of species with Tax ID not found: {len(not_found_species)}")

    tax_ids = {}
    for species in tqdm(found_species, desc='Retriving taxids'):
        taxid = tax_df[tax_df['name'] == species]['taxid'].values[0]
        tax_ids[species] = taxid

    return tax_ids


def get_taxids_from_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get a list of taxids from a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with microbiome data from which to extract the taxids.

    Returns
    -------
    tax_ids : pd.DataFrame
        Dataframe of name of species and taxids
    """
    species = get_microrganism_list(df)

    tax_ids = get_taxid(species)

    tax_ids = pd.DataFrame(tax_ids.items(), columns=['Species', 'TaxID'])
    tax_ids.set_index('Species', inplace=True)
    tax_ids = tax_ids.astype(int)

    return tax_ids


def get_proteome_for_taxid(taxid: str, max_tries:  int = 3):
    tries = 0
    url = f'https://rest.uniprot.org/uniprotkb/stream?format=fasta&query=taxonomy_id:{taxid}'
    while tries < max_tries:
        try:
            return requests.get(url).content.decode('utf8')
        except:
            print(f'Failed! {max_tries - tries} tries remaining.')
            tries += 1
            sleep(10)


def get_proteomes_from_df (df:pd.DataFrame, output_folder: str) -> None:
    """
    Get proteomes from a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with microbiome data from which to extract the proteomes.
    """
    tax_ids = get_taxids_from_df(df)

    output_path = Path.cwd()
    output_path = output_path / output_folder
    os.mkdir(output_path)

    for spec in tqdm(tax_ids.index, desc='Downloading proteomes'):
        proteome = get_proteome_for_taxid(tax_ids.loc[spec].values[0])
        with open(f'{output_folder}/{spec.replace(" ", "_")}.fasta', 'w') as f:
            f.write(proteome)
