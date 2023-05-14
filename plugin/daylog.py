import vim
import os
import datetime
import yaml
from utils import check_daylog_file

daylog_dir = os.path.expanduser('~/.daylog_notes')
today = datetime.datetime.now().strftime('%d-%m-%Y')
file_path = os.path.join(daylog_dir, f'{today}.yaml')

def create_daylog_dir():
    if not os.path.exists(daylog_dir):
        os.makedirs(daylog_dir)

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
    view_daylog(args='all')

def toggle_task_status(task_number):
    task_number = task_number.strip()
    task_number = int(task_number)
    data = check_daylog_file(file_path)

    if data is None:
        vim.command('echo "No daylog for today! You can create one with :NewDaylog"')
        return

    if task_number > len(data['tasks']) or task_number < 1:
        vim.command('echo "Invalid task number!"')
        return

    data['tasks'][task_number - 1]['status'] = not data['tasks'][task_number - 1]['status']
    
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

    vim.command('echo "I toggled the status of task {}"'.format(task_number))
    vim.command('bd')
    view_daylog(args='all')


def view_daylog(args=None):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        if data is None:
            vim.command('echo "No daylog for today!"')

        else:
            vim.command("new Daylog\'s {}".format(today))
            buf = vim.current.buffer
            del buf[:]

            for i, task in enumerate(data['tasks']):
                status = '\u2713' if task['status'] else " "
                title = task['title']

                if args == 'done':
                    if task['status']:
                        buf.append(f"{i + 1}. ({status}) {title}")

                elif args == 'not_done':
                    if not task['status']:
                        buf.append(f"{i + 1}. ({status}) {title}")

                elif args == 'all':
                    buf.append(f"{i + 1}. ({status}) {title}")

                else:
                    vim.command('echo "Invalid argument!"')
                    return

            vim.command("setlocal buftype=nofile")
            vim.command("setlocal bufhidden=hide")
            vim.command("setlocal nobuflisted")
            vim.command("setlocal nowrap")
            vim.command("setlocal nonumber")
            vim.command("setlocal norelativenumber")
            vim.command("setlocal foldlevel=0")
            vim.command("setlocal foldcolumn=0")
            vim.command("setlocal signcolumn=yes")

    else:
        vim.command('echo "I don\'s see a daylog for today! You can create one with :NewDaylog"')