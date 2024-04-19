import pandas as pd
from biomeanalyzer.legend.legend import get_treatments, add_treatments, microorganism_index
from biomeanalyzer.normalization.copy_normalization import normalize_data

def data_to_csv(df, legend_df, path_output, normalize=True):

    if normalize == True:
        data = normalize_data(df)
    else:
        data = df

    data = add_treatments(data, legend_df)
    data = microorganism_index(data)

    return pd.DataFrame.to_csv(data, path_output, sep="\t")

# %%

