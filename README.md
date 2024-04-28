# Process automation

This repo is designed to assist in structuring automation projects. The project is designed to produce a specified set of outputs based on an `output set` - these outputs can be Excel, PDF, CSV, graphs, etc. Each set of outputs will be produced in a single run. The output functions call an input function (to load all inputs required, including data and any templates), then a calculation function called (to perform any calculations on data as needed, note that the calculation function also calls on the input function to ensure all data required for the calculation is available).

The project is designed as a skeleton, items like database connections will need to be setup by yourself.

# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Clone the repository

To clone the repo from github, open a gitbash terminal and navigate to where you would like to install the folders, then run the command:

```bash
git clone https://github.com/tyefraser/photo_converter.git
```

## Create the virtual environment and load requirements

The venv will ensure you have the correct dependencies when running the code. To create the virtual environment make sure you have the `virtualenv` installed by running the following in gitbash:

```bash
pip install virtualenv
```

Now create the venv folder within your repo (make sure you cd into the repo folder):

```bash
python -m venv venv
```

This should create the venv folder within your repo. You will now need to activate the environment:

```bash
source venv/Scripts/activate
```

 You should now see a `(venv)` at the top of your terminal line:

```bash
(venv)
user@your_pc MINGW64 ~/github_projects/process_automation (main)
$
```

You can now install the requirements listed in the `requirements.txt` file:

```bash
(venv)
user@your_pc MINGW64 ~/github_projects/process_automation (main)
$pip install -r requirements.txt
```

Note: You can use git freeze to save the required packages from your project:

```bash
pip freeze > requirements.txt
```

## Test setup is complete

Now that you have loaded the repo and the requirements within the venv environment, you can test that the code works by running the following within the gitbash terminal:

```bash
python main.py -s set_1 -d 2022-01-01
```

If this doesn't work, please review the steps above or consult Google/chatGPT for assistance, noting that there can be differences between operating systems etc. that may cause issues.

# File Structure

## Main.py

The `main.py` file is the initiation point for the complete automation process. At the bottom you can see there is a  `parse_arguments()` function that will place all of the arguments entered into the `args` variable. These arguments can then be passed into the main function, for example the `set_name` variable is passed into `main` using `args.set_name`.

The `main` function then runs based on the arguments provided. There is initially a `setup_processes()` function that can be used to set up all required connections and folders. Currently this cleans out and creates the local folders where data, inputs and outputs are saved to. You can moodify this as required for your purposes. Note that the `setup` folder contains a `setup_config.yaml` file that you can modify with your specific needs. You can also add any passwords or anything to separate files (make sure you gitignore passwords and encrypt them on your local files too)

Next the code will run the main automation processes, this is designed into the following stages:

### Outputs function

The `outputs_fn` is used to generate the outputs required for a specified set. When designing your project, first work out what outputs you would need to produce in each run. For example, in the `\generate_outputs\output_configuration.yaml` file there is a list of accepted sets and then the outputs produced for those sets. Lets note `set_1` contains the `stratification` output, and we will follow how this works.

When the `outputs_fn` function runs, it gets the set required as an input, it will check this is a valid set then it will get a list of the required outputs and then loop through each one and run the `create_output` for each output. Note, this is designed such that all outputs listed must be valid and flow through the `if else` statements within the `create_output` function - if the report isnt valid there should be an error noted.

Each output will then have its own function script contained within the 
`generate_outputs\output_functions\` folder, for example `stratification_report.py`. This script contains the `generate_stratifications_report` function, which will generate the stratification report. This will be one of the output reports you want to generate.

At the top of `generate_stratifications_report` you will note that the function runs the `load_inputs` and `perform_calcs` functions. These are detailed more below, but basically they will load any direct inputs and perform calculations required for the stratification report. In the inputs function this will just load the report template required. In the calculation function, it just runs the calculation required to generate values for the stratification report. Note that the calculation function will also run the inputs function to obtain the inputs required for that specific calculation - therefore you do not need to list those inputs directly in the report generating function. Basically, to generate the report you would need some inputs like a template and some calculated values, this is achieved through running:
- load_inputs: loads any direct inputs, for example the report template. This could also be any direct data inputs, such as tables, that dont need any calculations performed period to putting them within the template
- perform_calcs: Perform any calculations required to get values used to populate the report. In order to perform the calculation, the calculation script will also run another iteration of hte load inputs function to obtain all data required for that specific calculation (allowing the code to be modular)

After the above has run, all of the data and files required to generate the report are available. The code should then generate the output required. In this case the code just adds the calculated values to excel template in the cells specified, and then saves the output to the repo. In your case you may want it to save to a database or other location.

Once this is done the output has been produced as required. The process will continue looping through the required outputs and produce them all as required. You may need to modify the process to include additional arguments, functions, tools, and setpup to achieve your goal, however the general structure should assist you in achieving this.

It is also noted that the process has been designed to be simple and easy to understand as well as modular. The process could be designed to run multiple sets in one go, however this would require additional consideration of how sets may interact or impact each other - therefore this has been avoided. If you have the capabilities, you could run each set in parallel at the same time. The functions are also designed to save all original inputs and calculations such that they are available for other reports when they run in the process (thereby not needing to re-load data or re-perform calculations). Again, there can be more efficient ways to achieve this based on your circumstances, however this process is designed to be easy to understand and use across many projects.