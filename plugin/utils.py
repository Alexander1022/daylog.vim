import vim
import os
import yaml

def check_daylog_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return data

    else:
        return None