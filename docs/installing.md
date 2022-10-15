#Installing PMTW

PMTW supports Python 3.7+. The recommended way to install PMTW is via pip.

pip install pmtw

!!!Note

	Depending on your system, you may need to use `pip3` to install packages 
	for Python 3.

!!!Warning

	Avoid using `sudo` to install packages. Do you really trust this package?

For instructions on installing Python and pip see "The Hitchhiker's Guide to 
Python" [Installation Guides](https://docs.python-guide.org/en/latest/starting/installation/).

##Updating PMTW

PMTW can be updated by running:

```sh
pip install --upgrade pmtw
```

##Installing Older Versions
Older versions of PRAW can be installed by specifying the version number as 
part of the installation command:

```
pip install pmtw==0.2.1
```