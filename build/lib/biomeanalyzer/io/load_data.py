import pandas as pd
import os
from pathlib import Path

def load_data(path_dataset):
    dataset = pd.read_csv(path_dataset, sep="\t", index_col=0)
    return dataset

def load_legend(path_legend):
    legend = pd.read_csv(path_legend, sep=";")
    return legend

def load_database():
    root_dir = Path(__file__).resolve().parent.parent.parent.parent
    database_path = root_dir / "database" / "16S_rRNA_copy_db" / "rrnDB-5.8_pantaxa_stats_NCBI.tsv"
    copy_number_db = pd.read_csv(database_path, sep="\t")
    return copy_number_db