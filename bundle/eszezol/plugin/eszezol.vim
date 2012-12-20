if exists("g:eszezol_loaded") || &cp
  finish
endif

let g:eszezol_loaded = 1

function! s:SetSyntax()
  if string(getline(1,5)) =~? '-\*- \{,1}python \{,1}-\*-'
    set syntax=python
  endif
endfunction

au BufReadPost * call s:SetSyntax()
