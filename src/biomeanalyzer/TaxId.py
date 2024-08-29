import pandas as pd
import importlib.resources as pkg_resources
from tqdm import tqdm


def get_microrganism_list (df:pd.DataFrame) -> list:     
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
    sum_df.drop(columns=["#NAME"], inplace=True)
    sum_df_splitted = pd.concat([split_data, sum_df], axis=1)

    def get_first_non_none_value(row):
        for col in ['#s', '#g', '#f', '#o', '#c', '#p', '#k']:
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

    print(f'\n Number of microorganisms present in this data: {len(species)}')
    
    return species


def get_taxid (species:list) -> list:
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
    print(f"\n Number of species with Tax ID found: {len(found_species)}")

    not_found_species = set(species) - set(found_species)
    print(f"\n Number of species with Tax ID not found: {len(not_found_species)}")

    tax_ids = []
    for species in tqdm(found_species):
        taxid = tax_df[tax_df['name'] == species]['taxid'].values[0]
        tax_ids.append(taxid)

    return tax_ids


def get_taxids_from_df (df:pd.DataFrame) -> list:
    """
    Get a list of taxids from a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with microbiome data from which to extract the taxids.

    Returns
    -------
    tax_ids : list
        List of taxids
    """
    species = get_microrganism_list(df)

    tax_ids = get_taxid(species)

    return tax_ids




