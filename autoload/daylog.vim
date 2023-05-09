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

function! ViewDaylog()
  python3 daylog.view_daylog()
endfunction

command! NewDaylog :call NewDaylog()
command! ViewDaylog :call ViewDaylog()