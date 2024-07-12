import pandas as pd
from biomeanalyzer.io.data_preparation import prepare_data_novogene
from biomeanalyzer.legend.legend import add_treatments #, microorganism_index
from biomeanalyzer.Normalization import normalize_data

def data_to_csv(df, meta_df, path_output, normalize=True, lab = "Novogene"):

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

    pd.DataFrame.to_csv(data, path_output + "/output_data.csv", sep=";", index=True)

    return f'Files saved in {path_output} as output_data.csv'

if __name__ == '__main__':
    data = pd.read_csv('/Users/tiago_silva/Documents/GitHub/BiomeAnalyzer/data/FullTaxa.species.percent.txt', sep='\t', index_col=0)
    legend = pd.read_csv('/Users/tiago_silva/Documents/GitHub/BiomeAnalyzer/data/Legenda_Indiv.csv', sep=';')
    data_to_csv(data, legend, path_output='.', normalize=True)