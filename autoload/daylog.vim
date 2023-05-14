if !has("python3")
  echo "vim has to be compiled with +python3 to run this"
  finish
endif

if exists('g:daylog_loaded')
  finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'plugin'))
sys.path.insert(0, python_root_dir)
import daylog
daylog.create_daylog_dir()
EOF

let g:daylog_loaded = 1

function! NewDaylog()
  python3 daylog.new_daylog()
endfunction

function! ViewDaylog(mode)
  python3 daylog.view_daylog(vim.eval('a:mode'))
endfunction

function! ToggleDaylog(task_number)
  if a:task_number =~ '\d'
    python3 daylog.toggle_task_status(vim.eval('a:task_number'))
  else
    echo "You have to enter a number."
  endif
  
endfunction

function! CloseDaylog()
  python3 daylog.close_daylog()
endfunction

command! NewDaylog :call NewDaylog()
" TODO: have to fix this
command! -nargs=1 ViewDaylog :call ViewDaylog(<f-args>)
command! -nargs=1 ToggleDaylog :call ToggleDaylog(<f-args>)