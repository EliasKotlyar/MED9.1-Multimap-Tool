import os
import yaml

def read_yaml_file(file):
    '''
    Reads the content of a YAML file and returns the parsed data.

    Parameters:
    - file (str): The path to the YAML file.

    Returns:
    - dict: The parsed data from the YAML file.

    Raises:
    - Exception: If the specified YAML file does not exist in the working directory.
    - ValueError: If the YAML file is invalid.
    '''
    # Check if the YAML file exists
    if not os.path.isfile(file):
        raise Exception(f'Input file "{file}" not found in the specified working directory.')

    # Read the YAML file
    with open(file, 'r') as yaml_file:
        try:
            data = yaml.safe_load(yaml_file)
        except yaml.YAMLError:
            raise ValueError("Error: Invalid YAML file")

    return data
