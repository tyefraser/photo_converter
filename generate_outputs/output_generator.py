from utils import prepare_path, read_yaml
from generate_outputs.output_functions.stratification_report import generate_stratifications_report


def create_output(
        output_set,
        required_output,
):
    
    if required_output == "payments":
        print("Run function")
    elif required_output == "report":
        print("Run function")
    elif required_output == "stratification":
        print("Run function")
        generate_stratifications_report(output_set=output_set)
    else:
        print("Error, invalid required report provided")
        print(f"Please ensure {required_output} should be in the create output function or not")
    

def outputs_fn(
        output_set
):
    # Read in output configuration yaml
    config_path = prepare_path("generate_outputs\output_configuration.yaml")
    output_config = read_yaml(config_path)

    # Return tracker
    ret = True

    # Check if the output set is valid
    if output_set not in output_config:
        available_sets = ', '.join(output_config.keys())
        print(f"Error: Output set '{output_set}' is not a valid set.")
        print(f"Please select from one of the following sets: {available_sets}")
        ret = False

    else:
        # Generate outputs
        for required_output in output_config[output_set]:
            create_output(
                output_set=output_set,
                required_output=required_output
            )

    return ret
