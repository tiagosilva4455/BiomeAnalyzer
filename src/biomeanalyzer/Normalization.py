from biomeanalyzer.LoadDatabase import load_database

def get_mean_copy_count(m):
    
    copy_number_db = load_database()

    taxa = m.split(";")
    n_taxa = len(taxa)-1
    name = taxa[n_taxa]

    try:
        if name.split(" ")[1] == "sp":
             name = name.strip() + "."
    except:
         pass

    while name.strip() not in copy_number_db['name'].values:
        n_taxa -= 1
        if n_taxa < 0:
            return 1
        name = taxa[n_taxa]

    if name.strip() in copy_number_db['name'].values:
        name = name.strip()
        # Retrieve the mean copy count for the microorganism
        mean_copy_count = copy_number_db.loc[copy_number_db['name'] == name, 'mean'].values[0]
        return mean_copy_count
    else:
        return 1  #that n was not found in the dataset, therefore the value will be it self (1)

def normalize_data(df):

    normalized_data = df.copy()

    #for n in df.index:
    #   normalized_data.loc[n] = df.loc[n] / get_mean_copy_count(n)
    normalized_data = normalized_data.apply(lambda row: row / get_mean_copy_count(row.name), axis=1)

    total_w_copies = normalized_data.sum()

    #for n in normalized_data.index:
    #    normalized_data.loc[n] = (100 * normalized_data.loc[n]) / total_w_copies
    normalized_data = normalized_data.apply(lambda row: (100 * row) / total_w_copies, axis=1)

    return normalized_data