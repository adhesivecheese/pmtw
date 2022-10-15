#!/usr/bin/env python
"""pmtw setup.py"""

import setuptools

if __name__ == "__main__":
    setuptools.setup()

"""
from setuptools import setup
from os import path
import re
from codecs import open

PACKAGE_NAME = "pmtw"
HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, "README.md"), encoding="utf-8") as fp:
    README = fp.read()
with open(path.join(HERE, PACKAGE_NAME, "constants.py"), encoding="utf-8") as fp:
    VERSION = re.search('__version__ = "([^"]+)"', fp.read()).group(1)

setup(
  name = PACKAGE_NAME,
  author = 'adhesiveCheese',
  author_email = 'adhesiveCheese@gmail.com',
  python_requires="~=3.7",
  classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
  ],
  description = (
        'PMTW, an acronym for "Python Moderator Toolbox Wrapper", is a python '
        "package that allows for simple access to Moderator Toolbox"
  ),
  install_requires=[
          'praw >=7.0',
  ],
  keywords = ['Reddit', 'Moderator_Toolbox', 'Web Wrapper'],
  license="Simplified BSD License",
  url = 'https://github.com/adhesivecheese/pmtw',
  download_url = 'https://github.com/adhesivecheese/pmtw/archive/refs/tags/v1_0_0.tar.gz',
  version = VERSION,
  long_description = README,

)
"""