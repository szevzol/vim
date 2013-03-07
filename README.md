vim
===

My vim configuration.

This repository serves as a portable configuration for me.
Feel free to use it but please beware of the fact that I didn't prepared it to be used by others.

Set up
----------

* Clone the repository. I usually put it in ~/etc. I use this as example in followings.

* Create ~/.vimrc. It should contain two lines:

```vim
let VIMDIR="~/etc/vim"
exec "source " . VIMDIR . "/rc/vimrc"
```

* Create ~/.vim as a symlink that points to the repository:

```sh
ln -s ~/etc/vim ~/.vim
```

* Create vimrc.private inside the repository. In the case of my example it will be ~/etc/vim/rc/vimrc.private. It should contain setting of runtimepath.
