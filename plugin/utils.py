import vim
import os
import yaml

# Checks if a daylog file exists for the current day
# Returns the data if it exists, None otherwise
def check_daylog_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return data

    else:
        return None

def create_file(file_path):
    with open(file_path, 'w'):
        pass

def check_date(date):
    try:
        day, month, year = date.split('-')

        if len(day) != 2 or len(month) != 2 or len(year) != 4:
            return False

        if not day.isnumeric() or not month.isnumeric() or not year.isnumeric():
            return False

        day = int(day)
        month = int(month)
        year = int(year)

        if day < 1 or day > 31 or month < 1 or month > 12 or year < 1:
            return False

        return True
    
    except ValueError:
        return False