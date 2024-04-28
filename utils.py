from pathlib import Path
import yaml
import pandas as pd

def get_project_root() -> Path:
    """
    Retrieve the project root directory.
    
    Returns:
        Path: The Path object representing the root directory of the project.
    """
    # Assuming that the root directory is two levels up from this file
    return Path(__file__).resolve().parent

def prepare_path(directory: str) -> Path:
    """
    Construct a full path by appending a specified directory to the project root.

    Args:
        directory (str): The directory to append to the project root.
    
    Returns:
        Path: The Path object representing the full path.
    """
    return str(get_project_root() / directory)


def read_yaml(
        yaml_file_path: str
):
    """
    reads a yaml file
    """
    if not (yaml_file_path.endswith((".yml", ".yaml"))):
        raise ValueError("Invalid file format. YAML file expected!")
    
    with open(yaml_file_path, "r") as file:
        return yaml.safe_load(file)


def combine_dataframes(df1, df2):
    # Find the union of both DataFrame columns and sort them
    all_columns = sorted(set(df1.columns).union(set(df2.columns)))

    # Reindex both dataframes to include all possible columns, filling missing data with NaN
    df1_aligned = df1.reindex(columns=all_columns)
    df2_aligned = df2.reindex(columns=all_columns)

    # Combine the two dataframes
    combined_df = pd.concat([df1_aligned, df2_aligned], ignore_index=True)
    
    return combined_df

