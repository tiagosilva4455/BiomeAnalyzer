import pandas as pd


def prepare_data_novogene(df):

    df = df.reset_index(drop=True)

    df['#NAME'] = df[('Taxonomy')].apply(clean_taxonomy)
    df = df.set_index("#NAME")
    df = df.drop(columns=['Taxonomy'])

    df = df * 100
    return df

def clean_taxonomy(taxonomy):
    parts = taxonomy.split(";")

    if parts[-1] == 's__':
        parts[-1] = parts[-2].replace("g__", "") + " sp"

    for i in range(len(parts)):
        if "__" in parts[i]:
            parts[i] = parts[i].split("__")[1]

    return ";".join(parts)