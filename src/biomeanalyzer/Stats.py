import pandas as pd
from scipy.stats import ttest_rel


def ttest_microorganisms(data: pd.DataFrame, group1: pd.DataFrame, group2: pd.DataFrame,
                         taxon_level: str) -> pd.DataFrame:
    """
    Perform a paired t-test to compare the growth of microorganisms between 2 groups.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe with microbiome data.
    group1 : pd.DataFrame
        List of columns for the first group.
    group2 : pd.DataFrame
        List of columns for the second group.
    taxon_level : str
        Taxonomic level of the data.

    Returns
    -------
    significant_microorganisms : pd.DataFrame
        Dataframe with the most significantly grown or declined microorganisms.

    """
    data_stats = data.copy()
    stats = pd.DataFrame()

    if data_stats.index[1] == "#CLASS":
        data_stats = data_stats[1:]  # this step will happen after normalization
    data_stats.columns = data_stats.columns.str.strip()  # Remove leading and trailing whitespaces from column names

    for col in group1 + group2:
        data_stats[col] = pd.to_numeric(data_stats[col],errors='coerce')
        # Convert all relevant columns to numeric, forcing errors to NaN

    if taxon_level == "species":
        # Check for repeated indexes and combine them
        data_stats = data_stats.groupby(data_stats["#NAME"]).sum()


    elif taxon_level == "genus":
        # Check if there are more than 5 ";" and remove extra ones
        def clean_name(name: str)->str:
            parts = name.split(";")
            if len(parts) > 6:
                return ";".join(parts[:6])
            return name

        data_stats.index = data_stats["#NAME"].map(clean_name)

        # Combine repeated indexes
        data_stats = data_stats.groupby(data_stats.index).sum()

    data_clean = data_stats.dropna(subset=group1 + group2)  # Drop rows with any NaN values

    g1_means = data_clean[group1].mean(axis=1)  # Calculate the mean for the 2 groups
    g2_means = data_clean[group2].mean(axis=1)

    stats['difference'] = g2_means - g1_means  # Calculate the difference (growth or decline)

    # Perform paired t-test to compare the growth between 2 groups
    t_stat, p_values = ttest_rel(data_clean[group1], data_clean[group2], axis=1)

    stats['p_value'] = p_values
    stats['#NAME'] = data_clean.index

    # Determine the direction of change (growth or decline)
    stats['direction'] = stats.apply(determine_direction, axis=1)

    # Filter for significant p-values (e.g., p < 0.05)
    significant_microorganisms = stats[stats['p_value'] < 0.05]

    # Sort by p-value
    significant_microorganisms = significant_microorganisms.sort_values(by='p_value')

    # Display the most significantly grown or declined microorganisms
    significant_microorganisms.set_index("#NAME", inplace=True)
    return significant_microorganisms


def determine_direction(row: pd.Series) -> str:
    """
    Determine the direction of change (growth or decline).

    Parameters
    ----------
    row : pd.Series
        Row of a DataFrame.

    Returns
    -------
    str
        The direction of change.

    """

    if row['p_value'] < 0.001:
        return '+++' if row['difference'] > 0 else '---'
    elif row['p_value'] < 0.01:
        return '++' if row['difference'] > 0 else '--'
    elif row['p_value'] < 0.05:
        return '+' if row['difference'] > 0 else '-'
    else:
        return 'growth' if row['difference'] > 0 else 'decline'

def clean_name(name: str, n_maintain:int) -> str: # Não uso isto em lado nenhum?
    """
    Clean the name.

    Parameters
    ----------
    name : str
        Name to be cleaned.
    """
    parts = name.split(";")
    if len(parts) > n_maintain:
        return ";".join(parts[:n_maintain])
    return name


def join_direction_df(dataframes: list[pd.DataFrame], dataframes_names=list[str]) -> pd.DataFrame:
    """
    Join DataFrames containing the direction of change for each group.

    Parameters
    ----------
    dataframes : list[pd.DataFrame]
        List of DataFrames containing the direction of change for each group.
    dataframes_names : list[str]
        List of names for each DataFrame.

    Returns
    -------
    result : pd.DataFrame
        DataFrame containing the direction of change for each group.

    """

    # Rename 'direction' column in each DataFrame
    if len(dataframes) == len(dataframes_names):
        for i in range(len(dataframes)):
            dataframes[i] = dataframes[i].rename(columns={'direction': f'direction_{dataframes_names[i]}'})
    else:
        raise ValueError('The number of DataFrames and DataFrames names must be the same')

        # Join the DataFrames
    result = dataframes[0][[f"direction_{dataframes_names[0]}"]]
    for i in range(1, len(dataframes)):
        result = result.join(dataframes[i][[f'direction_{dataframes_names[i]}']], how='outer')

    # Replace NaN values with an empty string
    result = result.fillna('')

    return result