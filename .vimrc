syntax on
map <F12> :VSTreeExplore <CR>
set tabstop=4
set shiftwidth=4
set smarttab
set softtabstop=4
set expandtab
set autoindent
autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class 
autocmd BufWritePre *.py normal m`:%s/\s\+$//e ``

