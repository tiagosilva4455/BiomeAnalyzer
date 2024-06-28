import pandas as pd
from scipy.stats import ttest_rel

def ttest_microorganisms (data:pd.DataFrame, group1:pd.DataFrame , group2:pd.DataFrame):

    data_stats = data.copy()
    stats = pd.DataFrame()

    if data_stats.index[1] == "#CLASS":
        data_stats = data_stats[1:] # this step will happen after normalization
    data_stats.columns = data_stats.columns.str.strip() # Remove leading and trailing whitespaces from column names
    
    for col in group1 + group2:
        data_stats[col] = pd.to_numeric(data_stats[col], errors='coerce') # Convert all relevant columns to numeric, forcing errors to NaN
    
    data_clean = data_stats.dropna(subset=group1 + group2)# Drop rows with any NaN values
    
    g1_means = data_clean[group1].mean(axis=1) # Calculate the mean for the 2 groups
    g2_means = data_clean[group2].mean(axis=1)
    
    stats['difference'] = g2_means - g1_means # Calculate the difference (growth or decline)
    
    # Perform paired t-test to compare the growth between 2 groups
    t_stat, p_values = ttest_rel(data_clean[group1], data_clean[group2], axis=1)

    stats['p_value'] = p_values
    stats['#NAME'] = data_clean['#NAME']

    # Determine the direction of change (growth or decline)
    stats['direction'] = stats.apply(determine_direction, axis=1)

    # Filter for significant p-values (e.g., p < 0.05)
    significant_microorganisms = stats[stats['p_value'] < 0.05]

    # Sort by p-value
    significant_microorganisms = significant_microorganisms.sort_values(by='p_value')

    # Display the most significantly grown or declined microorganisms
    significant_microorganisms[['#NAME', 'difference', 'direction', 'p_value']]
    significant_microorganisms.set_index("#NAME", inplace=True)
    return significant_microorganisms

def determine_direction(row):
    if row['p_value'] < 0.001:
        return '+++' if row['difference'] > 0 else '---'
    elif row['p_value'] < 0.01:
        return '++' if row['difference'] > 0 else '--'
    elif row['p_value'] < 0.05:
        return '+' if row['difference'] > 0 else '-'
    else:
        return 'growth' if row['difference'] > 0 else 'decline'