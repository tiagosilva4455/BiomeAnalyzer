import pandas as pd
def split_indiv_number(legend_df):
    legend_df[['Treatment', 'Indiv_legend']] = legend_df['Legend'].str.split('_', expand=True)
    return legend_df

def get_treatments(df, legend_df):

    legend_df = split_indiv_number(legend_df)

    treatment = {}

    for n in df.columns:
        n = n.split("-")[0]
        n = int(n)
        for i in legend_df["Indiv"]:
            i = int(i)
            if n == i:
                t = legend_df.loc[legend_df["Indiv"] == i, "Treatment"].values[0]
                treatment[n] = t

    return treatment

def add_treatments(df, legend_df):

    data = df.copy()  # create a new dataframe to avoid changing the original one

    treatment = get_treatments(df, legend_df)

    treatment_df = pd.DataFrame([treatment[int(c.split("-")[0])] for c in data.columns],columns=["Treatment"], index=data.columns)
    treatment_df = treatment_df.T

    data = pd.concat([data.iloc[:0], treatment_df, data.iloc[0:]])  # concatenate the new dataframe with the treatments to the original one at the first row
    return data


def index_microorgansim_names(df):

    names = []

    for m in df.index:

        taxa = m.split(";")
        n_taxa = len(taxa) - 1
        name = taxa[n_taxa]
        name = name.strip()

        try:
            if name.split(" ")[1] == "sp":
                name = name.strip() + "."
        except:
            pass

        while name.strip() == "Unclassified":
            n_taxa -= 1
            name = taxa[n_taxa]
            name = name.strip()

        if name.strip() != "No Hit":
            if name.strip() != "Treatment":
                if name.strip() == taxa[n_taxa - 1].strip():
                    name += " (1)"

        names.append(name)

    return names

def microorganism_index (df):
    names = index_microorgansim_names(df)
    df.index = names
    return df