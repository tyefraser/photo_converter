from inputs.input_loading import load_inputs
from utils import combine_dataframes

def generate_latest_loans_df():
    inputs_dict = load_inputs(inputs_to_load = [
        "existing_pool",
        "new_loans",
        "writeoffs",
    ])
    existing_pool = inputs_dict['existing_pool']
    new_loans = inputs_dict['new_loans']
    writeoffs = inputs_dict['writeoffs']
    
    # Find loan numbers to remove
    loans_to_remove = writeoffs['loan_number'].unique()

    # Filter out the rows where loan_number is in the list of loans to remove
    filtered_pool = existing_pool[
        ~existing_pool['loan_number'].isin(loans_to_remove)]
    
    latest_loans_df = combine_dataframes(
        df1=filtered_pool,
        df2=new_loans,
    )
    
    return latest_loans_df