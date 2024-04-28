import pandas as pd
from inputs.input_loading import load_inputs
from calculations.calc_functions.latest_loans import generate_latest_loans_df


def set_pool_statistics(
        output_set: str,
        latest_loans_df: pd.DataFrame,
):
    # Initiate set dictionary
    set_dict = {}

    # Get only the loans related to the current set
    set_latest_loans_df = latest_loans_df[latest_loans_df['pool'] == output_set].copy()

    # Generate the total balance
    set_dict['total_balance'] = set_latest_loans_df['current_balance'].sum()

    # Generate the total balance by category
    set_dict['category_A_balance'] = set_latest_loans_df[set_latest_loans_df['loan_category'] == 'A']['current_balance'].sum()
    set_dict['category_B_balance'] = set_latest_loans_df[set_latest_loans_df['loan_category'] == 'B']['current_balance'].sum()
    set_dict['category_C_balance'] = set_latest_loans_df[set_latest_loans_df['loan_category'] == 'C']['current_balance'].sum()
    set_dict['category_D_balance'] = set_latest_loans_df[set_latest_loans_df['loan_category'] == 'D']['current_balance'].sum()
    set_dict['category_E_balance'] = set_latest_loans_df[set_latest_loans_df['loan_category'] == 'E']['current_balance'].sum()
    set_dict['category_F_balance'] = set_latest_loans_df[set_latest_loans_df['loan_category'] == 'F']['current_balance'].sum()

    # Get the percentage of total balance for each loan category
    set_dict['category_A_percentage'] = set_dict['category_A_balance'] / set_dict['total_balance']
    set_dict['category_B_percentage'] = set_dict['category_B_balance'] / set_dict['total_balance']
    set_dict['category_C_percentage'] = set_dict['category_C_balance'] / set_dict['total_balance']
    set_dict['category_D_percentage'] = set_dict['category_D_balance'] / set_dict['total_balance']
    set_dict['category_E_percentage'] = set_dict['category_E_balance'] / set_dict['total_balance']
    set_dict['category_F_percentage'] = set_dict['category_F_balance'] / set_dict['total_balance']

    return set_dict


def pool_statistics(
        output_set: list,
):
    # Ensure all required inputs exist
    inputs_dict = load_inputs(inputs_to_load = [
        "existing_pool",
        "new_loans",
        "writeoffs",
    ])
    
    # Run generate_latest_loans_df as this is needed as an input
    # Note: this doesn't get added to calcs_dict as the functions need to be independent due to 
    # circular references
    latest_loans_df = generate_latest_loans_df()

    # Initiate pool statistics dictionary
    pool_statistics_dict = {}

    # Create pool statistics for each set
    pool_statistics_dict = set_pool_statistics(
        output_set=output_set,
        latest_loans_df=latest_loans_df,
    )

    return pool_statistics_dict
