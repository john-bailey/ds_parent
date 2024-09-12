# Check the ansible-devspace-poc/devfile projects value for a project, if not present add
# a new dict for the project.
import argparse
import yaml
import logging
import os
import sys

# logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
file_path = '/projects/ansible-devspaces-poc/devfile.yaml'

# Gather arguments
parser = argparse.ArgumentParser("add_to_devfile")
parser.add_argument("project_name", type=str)
parser.add_argument("git_username", type=str)
args = parser.parse_args()

if not args.project_name:
    logging.error("project_name is blank")
    sys.exit(os.EX_DATAERR)

if not args.git_username:
    logging.error("git_username is blank")
    sys.exit(os.EX_DATAERR)

project_name = args.project_name
remote = f"https://github.com/{args.git_username}/{project_name}.git"

logging.debug(f"{project_name}")
logging.debug(f"{remote}")

# Load existing .code-devfile json
with open(file_path) as file:
    devfile = yaml.safe_load(file)
logging.debug(devfile)

# Check if new project's name or path is present in the folder value
element_exists = False
for folder in devfile['projects']:
    logging.debug(folder)
    if folder.get("name") == project_name:
        logging.debug("Matching name found.")
        element_exists = True
        # sys.exit(os.EX_CONFIG)
        sys.exit(1)
    # if folder.get("path") == project_path:
    if folder["git"]["remotes"]["origin"] == remote:
        logging.debug("Matching remote found.")
        element_exists = True
        # sys.exit(os.EX_CONFIG)
        sys.exit(1)

if not element_exists:
    logging.debug("Element not found in projects. Adding new dict to list")
    new_project = {
        'name': project_name,
        'git': {
            'remotes': {
                'origin': remote
            }
        }
    }
    logging.debug(f"new project: {new_project}")
    devfile['projects'].append(new_project)
    
    # Write to file
    # yaml_devfile = yaml.dump(devfile, indent=4)
    with open(file_path, 'w') as file:
        yaml.safe_dump(devfile, file, default_flow_style=False, sort_keys=False)
        # yaml.safe_dump(devfile, file)
        # file.write(json_devfile)