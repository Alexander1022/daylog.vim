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
  python3 daylog.view(vim.eval('a:mode'))
endfunction

function ViewAll()
  python3 daylog.view()
endfunction

function! ToggleDaylog(task_number)
  if a:task_number =~ '\d'
    python3 daylog.toggle_task_status(vim.eval('a:task_number'))
  else
    echo "You have to enter a number."
  endif
endfunction

function! DeleteDaylog(task_number)
  if a:task_number =~ '\d'
    python3 daylog.delete_task(vim.eval('a:task_number'))
  else
    echo "You have to enter a number."
  endif
endfunction

function! DaylogsView()
  python3 daylog.list_of_daylogs()
endfunction

function! SetToday()
  python3 daylog.set_today()
endfunction

function! WipeDaylog()
  python3 daylog.wipe_daylog()
endfunction

function! SetDaylog(daylog_date)
  python3 daylog.set_daylog(vim.eval('a:daylog_date'))
endfunction

function! Prioritize(index, priority)
  python3 daylog.prioritize(vim.eval('a:index'), vim.eval('a:priority'))
endfunction

function! OrderDaylog()
  python3 daylog.order_daylog()
endfunction

" @command :NewDaylog
command! NewDaylog :call NewDaylog()
" @command :View <mode>
command! -nargs=1 View :call ViewDaylog(<f-args>)
" @command :Order 
command! Order :call OrderDaylog()
" @command :ViewAll
command! ViewAll :call ViewAll()
" @command :ToggleDaylog <entry_number>
command! -nargs=1 ToggleDaylog :call ToggleDaylog(<f-args>)
" @command :DeleteDaylog <entry_number>
command! -nargs=1 DeleteDaylog :call DeleteDaylog(<f-args>)

" @command :DaylogsList
command! DaylogsList :call DaylogsView()
" @command :SetToday
command! SetToday :call SetToday()
" @command :SetDaylog <daylog_date>
command! -nargs=1 SetDaylog :call SetDaylog(<f-args>)
" @command :WipeDaylog
command! WipeDaylog :call WipeDaylog()

" @command :Prioritize <index> <priority>
command! -nargs=* Prioritize :call Prioritize(<f-args>)