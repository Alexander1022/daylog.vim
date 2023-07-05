import vim
import os
import datetime
import yaml
from utils import check_daylog_file, create_file, check_date

daylog_dir = os.path.expanduser('~/.daylog_notes')
today = datetime.datetime.now().strftime('%d-%m-%Y')
file_path = os.path.join(daylog_dir, f'{today}.yaml')

def create_daylog_dir():
    if not os.path.exists(daylog_dir):
        os.makedirs(daylog_dir)

def set_today():
    global file_path
    file_path = os.path.join(daylog_dir, f'{today}.yaml')
    
    vim.command('echo "Daylog\'s date is set to {}"'.format(today))

def add_task(title):
    task_data = {'title': title, 'status': False}
    if not os.path.exists(file_path):
        create_file(file_path)

    with open(file_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    if data is None:
        data = {'tasks': []}
    data['tasks'].insert(0, task_data)
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

def wipe_daylog():
    prompt = vim.eval('input("Enter a date: ")')
    if check_date(prompt):
        file_path = os.path.join(daylog_dir, f'{prompt}.yaml')
        data = check_daylog_file(file_path)

        if data is None:
            vim.command('echo "There is not a log for this date!"')
            return

        f = open(file_path, 'r+')
        f.truncate()

        vim.command('bd')
        vim.command('echo "I wiped the daylog for {}"'.format(prompt))
        
        f.close()

def new_daylog():
    prompt = vim.eval('input("Entry: ")')
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
        vim.command('echo "Invalid entry number!"')
        return

    data['tasks'][task_number - 1]['status'] = not data['tasks'][task_number - 1]['status']
    
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

    vim.command('echo "I toggled the status of enrty {}"'.format(task_number))
    vim.command('bd')
    view_daylog(args='all')

def delete_task(task_number):
    task_number = task_number.strip()
    task_number = int(task_number)
    data = check_daylog_file(file_path)

    if data is None:
        vim.command('echo "No daylog for today! You can create one with :NewDaylog"')
        return

    if task_number > len(data['tasks']) or task_number < 1:
        vim.command('echo "Invalid entry number! Are you sure you\'re in the right daylog?"')
        return

    del data['tasks'][task_number - 1]

    with open(file_path, 'w') as file:
        yaml.dump(data, file)

    vim.command('echo "I deleted entry {}"'.format(task_number))
    vim.command('bd')
    view_daylog(args='all')

def view(args=None):
    vim.command('bd')

    if args == 'all':
        view_daylog(args='all')
    elif args == 'done':
        view_daylog(args='done')
    elif args == 'not_done':
        view_daylog(args='not_done')
    else:
        view_daylog(args=None)

def list_of_daylogs():
    yaml_files = [f for f in os.listdir(daylog_dir) if f.endswith(".yaml")]
    buf = vim.current.buffer
    del buf[:]
    
    for i, yaml_file in enumerate(yaml_files):
        buf.append(f"{i + 1}. {yaml_file}")

    if len(buf) > 0 and buf[0] == '':
        del buf[0]

    vim.command("setlocal laststatus=2")
    vim.command("setlocal title")
    vim.command('setlocal titlestring=Daylogs')
    vim.command("setlocal buftype=nofile")
    vim.command("setlocal bufhidden=hide")
    vim.command("setlocal nobuflisted")
    vim.command("setlocal nowrap")
    vim.command("setlocal nonumber")
    vim.command("setlocal norelativenumber")
    vim.command("setlocal foldlevel=0")
    vim.command("setlocal foldcolumn=0")
    vim.command("setlocal signcolumn=yes")
    vim.command("set cursorline")
    vim.command("highlight CursorLine cterm=NONE ctermbg=darkgrey ctermfg=white guibg=darkgrey guifg=white")
    vim.command('echo "Select a daylog to open it"')
    # Key mapping to open the selected daylog
    vim.command("nnoremap <buffer> <CR> :python3 daylog.handle_daylog_selection() <CR>")

# Open a selected daylog file
def handle_daylog_selection():
    line_number = vim.current.line
    if line_number:
        line_number = int(line_number.split(". ")[0])

        if line_number > 0:
            selected_line = vim.current.buffer[line_number - 1]
            selected_daylog = selected_line.split(". ")[1].strip()        
            
            vim.command("bd")

            global file_path
            file_path = os.path.join(daylog_dir, selected_daylog)

            view_daylog()

def set_daylog(daylog_date):
    if check_date(daylog_date):
        global file_path
        file_path = os.path.join(daylog_dir, f'{daylog_date}.yaml')
        create_file(file_path)

        data = check_daylog_file(file_path)
        if data is None:
            vim.command('echo "The file is created."')
            return

        vim.command('echo "The file is set."')
    
    else:
        vim.command('echo "Invalid date!"')

def view_daylog(args=None):
    data = check_daylog_file(file_path)

    if data is None:
        vim.command('echo "It looks like there is no entries here. You can create one with :NewDaylog"')
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

            elif args == 'all' or args == None:
                buf.append(f"{i + 1}. ({status}) {title}")

        vim.command("setlocal laststatus=2")
        vim.command("setlocal title")
        vim.command('setlocal titlestring=Daylog')
        vim.command("setlocal buftype=nofile")
        vim.command("setlocal bufhidden=hide")
        vim.command("setlocal nobuflisted")
        vim.command("setlocal nowrap")
        vim.command("setlocal nonumber")
        vim.command("setlocal norelativenumber")
        vim.command("setlocal foldlevel=0")
        vim.command("setlocal foldcolumn=0")
        vim.command("setlocal signcolumn=yes")