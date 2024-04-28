import os
import pandas as pd
import pickle
import shutil
# from common_utils import prepare_path
# from sharepoint_utils import get_sharepoint_file
# from sql_utils import query_as_pandas

from utils import prepare_path
from sharepoint.sharepoint_utils import get_sharepoint_file
from database.database_utils import query_as_pandas
from utils import read_yaml


def load_excel_sheet_as_df(file_path, sheet_name):
    print(f"Loading DataFrame from sheet '{sheet_name}' in file '{file_path}'")
    return pd.read_excel(file_path, sheet_name=sheet_name)


def source_inputs(
        input_config: dict,
):
    """
    Obtains the inputs from external sources
    """
    if input_config["source_type"] in ["sharepoint_df", "sharepoint_path"]:
        # Create file path
        file_path = prepare_path(
            os.path.join(input_config["to_location"], input_config["file_name"])
        )
        
        # Load file if it doesnt exist already
        # File could have loaded for other inputs, e.g. where different Excel
        # sheets are used
        if not os.path.exists(file_path):
            file_path
            # Load the file
            get_sharepoint_file(
                site_name=input_config["sharepoint_site"],
                sharepoint_url=input_config["sharepoint_site"]["url"],
                client_id=input_config["sharepoint_site"]["client_id"],
                client_secret=input_config["sharepoint_site"]["client_secret"],
                file_url=os.path.join(
                    input_config["sharepoint_folder"],
                    input_config["file_name"],
                ),
                to_location=input_config["to_location"],
            )

        # Check file size
        file_empty = False
        if os.stat(file_path).st_size == 0:
            print(f"File loaded is empty: {file_path}")
            file_empty = True

        # Load as df
        if input_config["source_type"] in ["sharepoint_df"]:
            if file_empty:
                return_input = pd.DataFrame()
            else:
                return_input = load_excel_sheet_as_df(
                    file_path=file_path,
                    sheet_name=input_config["sheet_name"],
                )

        # Load as file path
        elif input_config["source_type"] in ["sharepoint_path"]:
            return_input = file_path
        
        else:
            print("Error.")
    
    elif input_config["source_type"] in ["database_table"]:
        return_input = query_as_pandas()
    
    elif input_config["source_type"] in ["repo_file_df", "repo_file"]:
        print("Loading local repo file")
        
        # Create destination path variable
        destination_path = prepare_path(os.path.join(input_config["to_folder"], input_config["file_name"]))
        
        # Load file if it doesn't already exist
        if not os.path.exists(destination_path):
            # Create file path
            source_path = prepare_path(
                os.path.join(input_config["from_folder"], input_config["file_name"])
            )
        
            # Ensure file exists
            if os.path.exists(source_path):
                print(f"File exists, copying from {source_path} to {destination_path}")
                shutil.copy2(source_path, destination_path)
                print("Coping complete")
                
            else:
                print("Error: File does not exist")
        else:
            print(f"The file '{destination_path}' has already been loaded.")
        
        # Load as DataFrame
        if input_config["source_type"] in ["repo_file_df"]:
            print("Loading file as DataFrame")
            return_input = load_excel_sheet_as_df(
                file_path=destination_path,
                sheet_name=input_config["sheet_name"],
            )

        elif input_config["source_type"] in ["repo_file"]:
            return_input = destination_path

        # Keep file path
        if input_config["source_type"] in ["repo_file_only"]:
            return_input = destination_path

    else:
        print("Error: Input type not accepted.")

    return return_input

def load_inputs(
        inputs_to_load: list,
):
    """"
    Function to load the inputs as specified

    Inputs:
    inputs_list: list
        Lists the name of the inputs required
    
    Returns:
    inputs_dict:
        Dictionary of all inputs
    """
    # Load the existing dictionary if it exists
    inputs_dict_pickle_path = prepare_path("local_data/inputs_dict.pkl")
    if os.path.exists(inputs_dict_pickle_path):
        print("Inputs pickle exists - loading from pickle")
        with open(inputs_dict_pickle_path, "rb") as file:
            inputs_dict = pickle.load(file)
        print("Pickle loaded")

    else:
        print("Inputs dict created")
        inputs_dict = {}

    # Load inputs config
    input_config = read_yaml(
            yaml_file_path=prepare_path("inputs/input_config.yaml")
    )

    # Loop through the list of required inputs and load them if they dont
    # already exist
    existing_inputs = list(inputs_dict.keys())
    for input in inputs_to_load:
        if input not in existing_inputs:
            print(f"Sourcing {input}")
            inputs_dict[input] = source_inputs(input_config[input])
        else:
            print(f"Input '{input}' already loaded")

    # Save the dictionary for future use
    with open(inputs_dict_pickle_path, "wb") as file:
        pickle.dump(obj=inputs_dict, file=file)

    # Return the dictionary
    return inputs_dict
