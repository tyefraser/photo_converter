import os
import openpyxl

from utils import prepare_path
from inputs.input_loading import load_inputs
from calculations.perform_calcs import perform_calcs

def generate_stratifications_report(
        output_set: str
):
    # Load Direct inputs
    inputs_dict = load_inputs(inputs_to_load=["stratification_template"])

    # Perform required Calculations
    calcs_dict = perform_calcs(
        output_set=output_set,
        calcs_to_perform=["pool_statistics"],
    )

    # Load the workbook
    workbook = openpyxl.load_workbook(inputs_dict['stratification_template'])

    # Select the specified sheet by name
    sheet_name = 'Sheet1'
    if sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
    else:
        print(f"Sheet name '{sheet_name}' does not exist in the workbook.")
        return

    # Insert data into the Excel sheet
    sheet['C4'] = output_set
    sheet['C8'] = calcs_dict['pool_statistics']['total_balance'] # balances section
    sheet['C10'] = calcs_dict['pool_statistics']['category_A_balance']
    sheet['C11'] = calcs_dict['pool_statistics']['category_B_balance']
    sheet['C12'] = calcs_dict['pool_statistics']['category_C_balance']
    sheet['C13'] = calcs_dict['pool_statistics']['category_D_balance']
    sheet['C14'] = calcs_dict['pool_statistics']['category_E_balance']
    sheet['C15'] = calcs_dict['pool_statistics']['category_F_balance']
    sheet['C18'] = calcs_dict['pool_statistics']['category_A_percentage'] # Percentages section
    sheet['C19'] = calcs_dict['pool_statistics']['category_B_percentage']
    sheet['C20'] = calcs_dict['pool_statistics']['category_C_percentage']
    sheet['C21'] = calcs_dict['pool_statistics']['category_D_percentage']
    sheet['C22'] = calcs_dict['pool_statistics']['category_E_percentage']
    sheet['C23'] = calcs_dict['pool_statistics']['category_F_percentage']

    # Output file name
    output_file_name = f"{output_set}_stratification_report.xlsx"
    repo_output_folder = "local_outputs"
    repo_output_folder_path = prepare_path(repo_output_folder)
    output_file_name_path = os.path.join(repo_output_folder_path, output_file_name)
    
    # Save the workbook to a new file
    workbook.save(output_file_name_path)
    print(f"Excel file updated and saved to {output_file_name_path}")

    return calcs_dict
