let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd /mnt/pi/RPiMidiSC
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +2 Session.vim
badd +30 src/__main__.py
badd +64 src/Sequencing/Sequencer.py
badd +51 src/Ui/NewUserInterface.py
badd +66 src/Ui/UserInterface.py
badd +231 src/Sequencing/SaveLoad.py
badd +55 src/Hardware/OutputInterface.py
badd +14 notes.md
badd +0 /mnt/pi/RPiMidiSC
badd +71 ProjectManagement/Experiments/displayAnimInit.py
badd +70 src/config.py
badd +94 ProjectManagement/Experiments/displayTwinkle.py
badd +84 ProjectManagement/Experiments/displayAnimBackForth\ fixed.py
badd +38 Hardware/Blink.py
argglobal
%argdel
$argadd /mnt/pi/RPiMidiSC
edit src/__main__.py
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
wincmd _ | wincmd |
vsplit
2wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 35 + 37) / 74)
exe 'vert 1resize ' . ((&columns * 127 + 191) / 382)
exe '2resize ' . ((&lines * 36 + 37) / 74)
exe 'vert 2resize ' . ((&columns * 127 + 191) / 382)
exe 'vert 3resize ' . ((&columns * 126 + 191) / 382)
exe '4resize ' . ((&lines * 35 + 37) / 74)
exe 'vert 4resize ' . ((&columns * 127 + 191) / 382)
exe '5resize ' . ((&lines * 36 + 37) / 74)
exe 'vert 5resize ' . ((&columns * 127 + 191) / 382)
argglobal
balt src/Ui/UserInterface.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 31 - ((19 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 31
normal! 032|
wincmd w
argglobal
if bufexists(fnamemodify("notes.md", ":p")) | buffer notes.md | else | edit notes.md | endif
if &buftype ==# 'terminal'
  silent file notes.md
endif
balt src/__main__.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 9 - ((8 * winheight(0) + 18) / 36)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 9
normal! 08|
wincmd w
argglobal
if bufexists(fnamemodify("src/Hardware/OutputInterface.py", ":p")) | buffer src/Hardware/OutputInterface.py | else | edit src/Hardware/OutputInterface.py | endif
if &buftype ==# 'terminal'
  silent file src/Hardware/OutputInterface.py
endif
balt src/Sequencing/Sequencer.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 38 - ((30 * winheight(0) + 36) / 72)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 38
normal! 011|
wincmd w
argglobal
if bufexists(fnamemodify("src/Ui/UserInterface.py", ":p")) | buffer src/Ui/UserInterface.py | else | edit src/Ui/UserInterface.py | endif
if &buftype ==# 'terminal'
  silent file src/Ui/UserInterface.py
endif
balt src/Sequencing/Sequencer.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 117 - ((15 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 117
normal! 013|
wincmd w
argglobal
if bufexists(fnamemodify("src/config.py", ":p")) | buffer src/config.py | else | edit src/config.py | endif
if &buftype ==# 'terminal'
  silent file src/config.py
endif
balt Hardware/Blink.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 71 - ((33 * winheight(0) + 18) / 36)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 71
normal! 062|
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 35 + 37) / 74)
exe 'vert 1resize ' . ((&columns * 127 + 191) / 382)
exe '2resize ' . ((&lines * 36 + 37) / 74)
exe 'vert 2resize ' . ((&columns * 127 + 191) / 382)
exe 'vert 3resize ' . ((&columns * 126 + 191) / 382)
exe '4resize ' . ((&lines * 35 + 37) / 74)
exe 'vert 4resize ' . ((&columns * 127 + 191) / 382)
exe '5resize ' . ((&lines * 36 + 37) / 74)
exe 'vert 5resize ' . ((&columns * 127 + 191) / 382)
if exists(':tcd') == 2 | tcd /mnt/pi/RPiMidiSC | endif
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let &winminheight = s:save_winminheight
let &winminwidth = s:save_winminwidth
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
let g:this_session = v:this_session
let g:this_obsession = v:this_session
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
