import pandas as pd


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