from pathlib import Path
from biomeanalyzer.Normalization import normalize_data
import pandas as pd
import os



def read_file(path: str, type_data: str) -> pd.DataFrame:
    """
    Read a file into a pandas DataFrame.

    Parameters
    ----------
    path : str
        Path to the file.
    type_data : str
        Type of data in the file (either 'dataset' or 'metadata').

    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the data from the file.
    """
    # Determine the file extension and choose the appropriate pandas function
    if type_data == 'dataset':
        _, ext = os.path.splitext(path)
        if ext == '.xlsx':
            return pd.read_excel(path, engine='openpyxl', index_col=0 if type_data == 'dataset' else None)
        elif ext == '.xls':
            return pd.read_excel(path, engine='xlrd', index_col=0 if type_data == 'dataset' else None)
        else:
            return pd.read_csv(path, sep=";", index_col=0 if type_data == 'dataset' else None)

    if type_data == 'metadata':
        _, ext = os.path.splitext(path)
        if ext == '.xlsx':
            return pd.read_excel(path, engine='openpyxl', usecols = [0, 1, 2])
        elif ext == '.xlxt':
            return pd.read_excel(path, usecols = [0, 1, 2])


def load_data(path_dataset: str, path_metadata: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the dataset and metadata files into pandas DataFrames.

    Parameters
    ----------
    path_dataset : str
        Path to the dataset file.
    path_metadata : str
        Path to the metadata file.

    Returns
    -------
    dataset : pandas.DataFrame
        DataFrame containing the dataset.
    metadata : pandas.DataFrame
        DataFrame containing the metadata.
    """

    dataset = read_file(path_dataset, type_data='dataset')
    metadata = read_file(path_metadata, type_data='metadata')

    return dataset, metadata


def prepare_data_novogene(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the data from Novogene for analysis.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the dataset.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the dataset prepared for analysis.
    """

    df = df.reset_index(drop=True)

    df['#NAME'] = df['Taxonomy'].apply(clean_taxonomy)
    df = df.set_index("#NAME")
    df = df.drop(columns=['Taxonomy'])

    df = df * 100
    return df


def clean_taxonomy(taxonomy: str) -> str:
    """
    Clean the taxonomy string.

    Parameters
    ----------
    taxonomy : str
        Taxonomy string to be cleaned.

    Returns
    -------
    str
        Cleaned taxonomy string.
    """
    parts = taxonomy.split(";")

    if parts[-1] == 's__':
        parts[-1] = parts[-2].replace("g__", "") + " sp"

    for i in range(len(parts)):
        if "__" in parts[i]:
            parts[i] = parts[i].split("__")[1]

    return ";".join(parts)


def add_treatments(data_df: pd.DataFrame, meta_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add the treatments to the DataFrame.

    Parameters
    ----------
    data_df : pandas.DataFrame
        DataFrame containing the data.
    meta_df : pandas.DataFrame
        DataFrame containing the metadata.

    Returns
    -------
    updated_df : pandas.DataFrame
        DataFrame containing the data with the treatments added.

    """
    # Assuming treatments are to be used as values for the #CLASS row
    treatments = meta_df.iloc[:, 1].values

    # Create a DataFrame for the #CLASS row
    class_df = pd.DataFrame([treatments], columns=data_df.columns)
    class_df.index = ['#CLASS']

    # Concatenate the #CLASS row DataFrame with the original DataFrame
    updated_df = pd.concat([class_df, data_df], axis=0)
    updated_df.index.name = '#NAME'
    return updated_df


def arrange_data(df: pd.DataFrame, meta_df: pd.DataFrame, normalize: bool = True, lab: str = "Novogene") -> pd.DataFrame:
    """
    Arrange the data for analysis.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data.
    meta_df : pandas.DataFrame
        DataFrame containing the metadata.
    normalize : bool
        Whether to normalize the data or not.
    lab : str
        The lab that generated the data.

    Returns
    -------
    data : pandas.DataFrame
        DataFrame containing the data arranged for analysis.

    """
    if lab == "Novogene":
        df = prepare_data_novogene(df)
    elif lab == "RTL":
        pass

    if normalize == True:
        data = normalize_data(df)
    else:
        data = df

    data = data.astype(float)
    data = add_treatments(data, meta_df)

    return data


# DATA TO CSV (MICROBIOME ANALYST)
def data_to_csv(df: pd.DataFrame, meta_df: pd.DataFrame, normalize: bool = True, lab: str = "Novogene") -> str:
    """
    Save the data and metadata to CSV files.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data.
    meta_df : pandas.DataFrame
        DataFrame containing the metadata.
    normalize : bool
        Whether to normalize the data or not.
    lab : str
        The lab that generated the data.

    Returns
    -------
    str
        A message indicating the location of the saved files.
    """

    data = arrange_data(df, meta_df, normalize, lab)

    output_folder = Path.cwd()

    pd.DataFrame.to_csv(data, output_folder / "output_data.csv", sep=";", index=True)
    pd.DataFrame.to_csv(meta_df, output_folder / "output_metadata.csv", sep=";", index=False)

    return f'Files saved in {output_folder} as output_data.csv and output_metadata.csv'
