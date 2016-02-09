## Dev Stuff
### MacPorts
Install [MacPorts](https://www.macports.org), don't use Brew.

### XCode

### Editors
[my .vim repository](https://github.com/drsmithization/dotvim)

### Terminal
#### 
#### misc
```bash
function xman {
    man -t "$@" | open -f -a /Applications/Preview.app
}

export -f xman
```
Coloured ls:
```bash
alias ls='ls -G'
```

### Python
1) first, install proper Python 2.7, pip and virtualenv:
```bash
$ sudo port install python27
$ port select --list python
Available versions for python:
	none
	python26-apple
	python27
	python27-apple (active)
	python34
$ sudo port select --set python python27
$ sudo port install py27-pip
$ sudo port select --set pip pip27
$ sudo port install py27-virtualenv
$ sudo port select --set virtualenv virtualenv27
```
2) and setup the environment:
```bash
$ cat <<END >> ~/.bashrc
export VIRTUALENV_DISTRIBUTE=true
export PIP_VIRTUALENV_BASE=$HOME/.virtualenvs
export PIP_REQUIRE_VIRTUALENV=true
export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache
END

$ cd ~/.virtualenvs
$ virtualenv science
$ echo "source $HOME/.virtualenvs/science/bin/activate" >> ~/.bashrc
$ source ~/.bashrc
```

3) install libraries:
```bash
$ pip install --upgrade pip
$ pip install numpy
$ pip install scipy
$ pip install pandas
$ pip install sklearn
$ pip install matplotlib
$ pip install seaborn
$ pip install jupyter
```
