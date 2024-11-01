import pandas as pd
from biomeanalyzer.load_database import load_database


def get_mean_copy_count(m: str) -> float:
    """
    Get the mean copy count for a microorganism.

    Parameters
    ----------
    m : str
        Microorganism name.

    Returns
    -------
    mean_copy_count : float
        Mean copy count for the microorganism.

    """
    
    copy_number_db = load_database()

    taxa = m.split(";")
    n_taxa = len(taxa)-1
    name = taxa[n_taxa]

    try:
        if name.split(" ")[1] == "sp":
             name = name.strip() + "."
    except:
         pass

    while name.strip() not in copy_number_db['name'].values:
        n_taxa -= 1
        if n_taxa < 0:
            return 1
        name = taxa[n_taxa]

    if name.strip() in copy_number_db['name'].values:
        name = name.strip()
        # Retrieve the mean copy count for the microorganism
        mean_copy_count = copy_number_db.loc[copy_number_db['name'] == name, 'mean'].values[0]
        return mean_copy_count
    else:
        return 1  # that n was not found in the dataset, therefore the value will be it self (1)


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the data.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with microbiome data to be normalized.

    Returns
    -------
    normalized_data : pd.DataFrame
        Normalized data.

    """
    normalized_data = df.copy()
    normalized_data = normalized_data.apply(lambda row: row / get_mean_copy_count(row.name), axis=1)

    total_w_copies = normalized_data.sum()
    normalized_data = normalized_data.apply(lambda column: (100 * column) / total_w_copies, axis=1)

    return normalized_data