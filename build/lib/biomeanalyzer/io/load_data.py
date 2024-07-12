import pandas as pd
import os
from pathlib import Path

def load_data(path_dataset, path_metadata):
    dataset = pd.read_csv(path_dataset, sep=";", index_col=0)
    metadata = pd.read_csv(path_metadata, sep=";")
    return dataset, metadata

def load_database():
    root_dir = Path(__file__).resolve().parent.parent.parent.parent
    database_path = root_dir / "database" / "16S_rRNA_copy_db" / "rrnDB-5.8_pantaxa_stats_NCBI.tsv"
    copy_number_db = pd.read_csv(database_path, sep="\t")
    return copy_number_db
