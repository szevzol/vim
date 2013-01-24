vim
===

My vim configuration.

Setting up
----------

* Clone repo to anywhere. I usually put it in ~/etc. I use this as example in followings.

* Create ~/.vimrc. It should contain two things:

```vim
let VIMDIR="~/etc/vim"
exec "source " . VIMDIR . "/rc/vimrc"
```

* Create ~/.vim as a symlink that points to the vim repo:

```sh
ln -s ~/etc/vim ~/.vim
```

* Create vimrc.private inside the repo. In example it will be ~/etc/vim/rc/vimrc.private. It should contain setting of runtimepath.
