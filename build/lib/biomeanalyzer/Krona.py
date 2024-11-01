import subprocess
import pandas as pd
import os
import tempfile
import shutil
from pathlib import Path
from biomeanalyzer.Data_IO import arrange_data


def make_kronas(df: pd.DataFrame, meta_df: pd.DataFrame, normalize: bool = True, lab: str = "Novogene"):
    """
    Make Krona plots from the microbiome data.

    Parameters
    ----------
    df : pd.DataFrame
        The microbiome data.
    meta_df : pd.DataFrame
        The metadata.
    normalize : bool, optional
        Normalize the data, by default True.
    lab : str, optional
        The laboratory where the data was generated, by default
        "Novogene".

    Returns
    -------
    None
    """
    dataset = arrange_data(df, meta_df, normalize=normalize, lab=lab)

    temp_dir = tempfile.mkdtemp()  # Create a temporary directory to store the split files
    split_dataset(dataset, temp_dir)  # Split the dataset into multiple files
    temp_list = sorted([f for f in os.listdir(temp_dir) if f.endswith('.csv')])
    # List files in the temporary directory .csv
    input_file_list_path = os.path.join(temp_dir, 'input_files.txt')  # Make the absolute path to the file list

    # Write the list of input files to a file with their full paths
    with open(input_file_list_path, 'w') as file_list:
        for file_name in temp_list:
            file_list.write(f"{os.path.join(temp_dir, file_name)}\n")

    command = 'ktImportText'  # Krona command to run
    desktop = Path.home() / "Desktop" # Get the desktop path
    output_file = 'output_krona.html'  # Output file name

    # Construct the full command to run
    full_command = [command, '-o', output_file]
    # Add the input files to the command
    with open(input_file_list_path, 'r') as file_list:
        input_files = file_list.read().splitlines()
        full_command.extend(input_files)

    # Execute the command
    try:
        subprocess.run(full_command, check=True, cwd=temp_dir)
        print(f"Command '{command}' executed successfully. Krona {output_file} created.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing '{command}': {e}")
    except FileNotFoundError as e:
        print(f"An error occurred: {e}")

    # Move the Krona to the desktop
    try:
        output_file_path = os.path.join(temp_dir, output_file)
        output_folder = Path.cwd()
        shutil.move(output_file_path, output_folder)
        print(f"Krona moved to {output_folder}")
    except Exception as e:
        print(f"An error occurred while moving the Krona to the desktop: {e}")

    # Delete the temporary directory
    shutil.rmtree(temp_dir)
    print(f"Temporary working directory {temp_dir} deleted")


def split_dataset(dataset: pd.DataFrame, path: str)-> None:
    """
    Split the dataset into multiple files.

    Parameters
    ----------
    dataset : pd.DataFrame
        The dataset to split.
    path : str
        The path to save the split files.

    Returns
    -------
    None
    """

    data_to_split = split_taxonomy(dataset)

    for col_name in data_to_split.columns[:-7]:
        df = data_to_split[[col_name, '#k', '#p', '#c', '#o', '#f', '#g']]
        df.to_csv(f"{path}/{col_name}.csv", sep="\t", index=False, header=False)


def split_taxonomy(dataset):
    """
    Split the taxonomy of the dataset.

    Parameters
    ----------
    dataset : pd.DataFrame
        The dataset to split.

    Returns
    -------
    pd.DataFrame
        The dataset with the taxonomy split.

    """
    data_copy = dataset.copy() # Copy the dataset to avoid modifying the original

    if '#CLASS' in dataset.columns:
        data_copy = data_copy.drop(index=["#CLASS"])  # get rid of the row #CLASS

    data_copy = data_copy.reset_index(drop=False)  # get the names of the microrganisms

    split_data = data_copy['#NAME'].str.split(';', expand=True)
    split_data = split_data.fillna('')
    split_data = split_data.rename(columns={0: '#k', 1: '#p', 2: '#c', 3: '#o', 4: '#f', 5: '#g', 6: '#s'})
    split_data = split_data.map(clean_taxons)

    data_copy.drop(columns=["#NAME"], inplace=True)

    krona_data = pd.concat([data_copy, split_data], axis=1)

    return krona_data


def clean_taxons(string: str) -> str:
    """
    Clean the taxons.

    Parameters
    ----------
    string : str
        The string to clean.

    Returns
    -------
    str
        The cleaned string.
    """
    if string == "s__":
        string = "sp."
    elif "__" in string:
        return string.split("__")[1]
    return string
