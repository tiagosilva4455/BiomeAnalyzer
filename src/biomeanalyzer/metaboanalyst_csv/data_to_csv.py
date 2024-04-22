import pandas as pd
from biomeanalyzer.legend.legend import add_treatments #, microorganism_index
from biomeanalyzer.normalization.copy_normalization import normalize_data

def data_to_csv(df, legend_df, path_output, normalize=True):

    if normalize == True:
        data = normalize_data(df)
    else:
        data = df

    data = add_treatments(data, legend_df)

    data_copy = data.reset_index()
    data_copy = data_copy.rename(columns={'index': '#NAME'})

    legend = legend_df.drop(legend_df.columns[0], axis=1)
    legend['Indiv'] = legend['Indiv'].apply(lambda x: str(x) + '-MS515F')

    pd.DataFrame.to_csv(data_copy, path_output + "output_data.csv", sep=",", index=False)
    pd.DataFrame.to_csv(legend, path_output + "output_metadeta.csv", sep=",", index=False)

    return f'Files saved in {path_output} as output_data.csv and output_metadata.csv'


