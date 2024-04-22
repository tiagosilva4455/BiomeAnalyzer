import pandas as pd
from biomeanalyzer.legend.legend import add_treatments #, microorganism_index
from biomeanalyzer.normalization.copy_normalization import normalize_data

def data_to_csv(df, legend_df, path_output, normalize=True):

    if normalize == True:
        data = normalize_data(df)
    else:
        data = df

    data_copy = data.reset_index()
    data_copy = data_copy.rename(columns={'index': '#NAME'})
    data_copy = add_treatments(data_copy, legend_df)

    return pd.DataFrame.to_csv(data_copy, path_output, sep="\t")

# %%

