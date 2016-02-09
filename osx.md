## Dev Stuff
### MacPorts
Install [MacPorts](https://www.macports.org), don't use Brew.

### XCode

### Python
First, install proper Python 2.7, pip and virtualenv:
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
