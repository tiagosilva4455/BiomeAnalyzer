import pandas as pd
from pathlib import Path


def load_database():
    root_dir = Path(__file__).resolve().parent.parent.parent
    database_path = root_dir / "database" / "16S_rRNA_copy_db" / "rrnDB-5.8_pantaxa_stats_NCBI.tsv"
    copy_number_db = pd.read_csv(database_path, sep="\t")
    return copy_number_db
