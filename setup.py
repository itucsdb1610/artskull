from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='artskull-ituscdb1610-app',
    version='1.0.0',
    description='App for db class',
    long_description=long_description,
    url='https://github.com/itucsdb1610/itucsdb1610'
)