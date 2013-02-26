 let g:clang_complete_auto = 0
 let g:clang_library_path = "/proj/cudbdm/tools/external/clang-latest/lib"
 let g:clang_use_library = 1
 let g:clang_complete_copen = 1
 let g:clang_hl_errors = 0
 " Do not update QF periodically, as Vim may get stuck because of it
 let g:clang_periodic_quickfix = 0
 let g:clang_user_options = "-Wall"
 
 " Toggle QF update by hitting F8
 nnoremap <silent> <F10> :call g:ClangUpdateQuickFix()<CR>
 
 let g:SuperTabDefaultCompletionType = "context"

 let g:clang_debug = 1
