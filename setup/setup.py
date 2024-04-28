import os
import shutil
from utils import prepare_path, read_yaml


def refresh_folders(folder_path):
    """Create a folder if it does not already exist, or clear it by deleting and recreating it if it does."""
    try:
        if os.path.exists(folder_path):
            # Remove the entire directory
            shutil.rmtree(folder_path)
            print(f"Folder cleared by deleting: {folder_path}")
            # Recreate the directory
            os.makedirs(folder_path)
            print(f"Folder recreated: {folder_path}")
        else:
            # Create the directory as it does not exist
            os.makedirs(folder_path)
            print(f"Folder created: {folder_path}")
    except Exception as e:
        print(f"An error occurred while creating or clearing the folder: {e}")


def setup_processes():
    # Read in setup config
    setup_config = read_yaml(prepare_path("setup\setup_config.yaml"))

    
    # Create folders that are required
    for folder in setup_config["required_repo_folders"]:
        refresh_folders(prepare_path(folder))
        ## TO DO: Remove any files that are in these folders as well - start from scratch
    
    
    
