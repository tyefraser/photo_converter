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

from calculations.calc_functions.pool_statistics import pool_statistics
from calculations.calc_functions.latest_loans import generate_latest_loans_df

def run_calculation(
        output_set: list,
        calc: str,
):
    print(f"Performing '{calc}' calc")
    calc_dict = {} ## To delete
    
    if calc == "latest_loans":
        calc_dict["latest_loans"] = generate_latest_loans_df()
        
    if calc == "pool_statistics":
        calc_dict["pool_statistics"] = pool_statistics(output_set)
    
    return calc_dict


def perform_calcs(
        output_set: list,
        calcs_to_perform: list,
):
    # Load the existing dictionary if it exists
    calcs_dict_pickle_path = prepare_path("local_data/calcs_dict.pkl")
    if os.path.exists(calcs_dict_pickle_path):
        print("calcs pickle exists - loading from pickle")
        with open(calcs_dict_pickle_path, "rb") as file:
            calcs_dict = pickle.load(file)
        print("Pickle loaded")

    else:
        print("calcs dict created")
        calcs_dict = {}

    # Loop through the list of required calcs and load them if they dont
    # already exist
    existing_calcs = list(calcs_dict.keys())
    for calc in calcs_to_perform:
        if calc not in existing_calcs:
            print(f"Performing calculation: {calc}")
            calcs_dict.update(run_calculation(
                output_set=output_set,
                calc=calc
            ))
            
        else:
            print(f"calc '{calc}' already loaded")

    # Save the dictionary for future use
    with open(calcs_dict_pickle_path, "wb") as file:
        pickle.dump(obj=calcs_dict, file=file)

    # Return the dictionary
    return calcs_dict
