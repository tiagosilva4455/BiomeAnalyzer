import pandas as pd
import importlib.resources as pkg_resources


def load_database():
    """
    Load the database with the copy number of rRNA genes from the rrnDB database.

    Returns
    -------
    copy_number_db : pd.DataFrame
        Dataframe with the copy number of rRNA genes
    """
    db_path = pkg_resources.files("biomeanalyzer") / "data" / "rrnDB-5.8_pantaxa_stats_NCBI.tsv"
    database_path = str(db_path)
    copy_number_db = pd.read_csv(database_path, sep="\t")
    return copy_number_db
