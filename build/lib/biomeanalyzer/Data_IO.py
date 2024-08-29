
from pathlib import Path
from biomeanalyzer.Normalization import normalize_data
import pandas as pd
import os


def load_data(path_dataset, path_metadata):
    # Determine the file extension and choose the appropriate pandas function
    def read_file(path, type_data):
        _, ext = os.path.splitext(path)
        if ext == '.xlsx':
            return pd.read_excel(path, engine='openpyxl', index_col=0 if type_data == 'dataset' else None)
        elif ext == '.xls':
            return pd.read_excel(path, engine='xlrd', index_col=0 if type_data == 'dataset' else None)
        else:
            return pd.read_csv(path, sep=";", index_col=0 if type_data == 'dataset' else None)

    dataset = read_file(path_dataset, type_data='dataset')
    metadata = read_file(path_metadata, type_data='metadata')

    return dataset, metadata


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


#ADD COLUMN #CLASS
def add_treatments(data_df, meta_df):
    # Assuming treatments are to be used as values for the #CLASS row
    treatments = meta_df['Treatment'].values

    # Create a DataFrame for the #CLASS row
    class_df = pd.DataFrame([treatments], columns=data_df.columns)
    class_df.index = ['#CLASS']

    # Concatenate the #CLASS row DataFrame with the original DataFrame
    updated_df = pd.concat([class_df, data_df], axis=0)
    updated_df.index.name = '#NAME'
    return updated_df


def arrange_data(df, meta_df, normalize=True, lab="Novogene"):
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


#DATA TO CSV (MICROBIOME ANALYST)
def data_to_csv(df, meta_df, normalize=True, lab="Novogene"):

    data = arrange_data(df, meta_df, normalize, lab)

    output_folder = Path.cwd()

    pd.DataFrame.to_csv(data, output_folder / "output_data.csv", sep=";", index=True)

    return f'Files saved in {output_folder} as output_data.csv'
