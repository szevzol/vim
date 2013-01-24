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

* Create symlink ~/.vim that will link to the vim repo:

```sh
ln -s ~/etc/vim ~/.vim
```

* Create ~/etc/vim/rc/vimrc.private. It should contain setting of runtimepath.
