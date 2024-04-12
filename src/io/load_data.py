import pandas as pd

def load_data(path_dataset):
    dataset = pd.read_csv(path_dataset, sep="\t", index_col=0)
    return dataset

def load_legend(path_legend):
    legend = pd.read_csv(path_legend, sep=";")
    return legend