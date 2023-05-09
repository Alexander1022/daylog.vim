import vim
import os
import datetime
import yaml

daylog_dir = os.path.expanduser('~/.daylog_notes')
today = datetime.datetime.now().strftime('%d-%m-%Y')
file_path = os.path.join(daylog_dir, f'{today}.yaml')

def create_daylog_dir():
    if not os.path.exists(daylog_dir):
        os.makedirs(daylog_dir)

# this function can be written better
def add_task(title):
    task_data = {'title': title, 'status': False}
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass

    with open(file_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    if data is None:
        data = {'tasks': []}
    data['tasks'].insert(0, task_data)
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

def new_daylog():
    prompt = vim.eval('input("Enter today\'s note: ")')
    add_task(prompt)
    vim.command('echo "Created daylog!"')

def view_daylog():
    vim.command('echo "View daylog"')