#! /usr/bin/env python3

import json
import yaml
import os

def parse_json_file(file_path):
    """
    Parses a JSON file and returns the data as a Python object.

    :param file_path: Path to the JSON file.
    :return: Parsed JSON data as a Python object, or None if an error occurs.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON - {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def create_collab_yaml(name, data):
    """
    Creates a YAML file with the data from a parsed JSON object.

    :param data: Parsed JSON data as a Python object.
    """
    if not data:
        return
    yaml_data = {}
    for collab in data:
        if collab['type'] != 'User':
            continue
        if 'login' not in collab:
            print("Error: Missing 'name' field in JSON data.")
            return
        else:
            auth = get_permissions(collab['permissions'])
            yaml_data[name] = {collab['login']: {'type': 'user', 'permissions': auth}}
    print("YAML data:")
    print(yaml_data)

    try:
        with open(f'{name}.yaml', 'w') as file:
            yaml.dump(yaml_data, file)
        print("YAML file created successfully.")
    except Exception as e:
        print(f"Error: Failed to create YAML file - {e}")

def get_permissions(collab_permissions):
    print("collab_permissions:")
    print(collab_permissions)
    auth = ""
    if collab_permissions['admin'] == True:
        auth = "admin"
    elif collab_permissions['maintain'] == True:
        auth = "maintain"
    elif collab_permissions['push'] == True:
        auth = "write"
    elif collab_permissions['triage'] == True:
        auth = "write"
    elif collab_permissions['pull'] == True:
        auth = "read"
    return auth

def main(path):
    """
    Main function to demonstrate the usage of parse_json_file.
    """
    directory = os.fsencode(path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"): 
            print(os.path.join(directory, filename))
            data = parse_json_file(os.path.join(directory, filename))
            if len(data) > 0:
                create_collab_yaml(os.path.splitext(filename)[0], data)
            continue
        else:
            continue

if __name__ == "__main__":
    main('../collabs')
