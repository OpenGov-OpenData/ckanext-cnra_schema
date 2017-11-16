CNRA Schema
===========

Requirements
------------
Requires [ckanext-scheming](https://github.com/ckan/ckanext-scheming)


Installation
------------
To install ckanext-cnra_schema for development, activate your CKAN virtualenv and do::

    git clone https://github.com/OpenGov-OpenData/ckanext-cnra_schema.git
    cd ckanext-cnra_schema
    python setup.py develop
    pip install -r requirements.txt


Config settings
---------------
```ini

ckan.plugins = ... cnra_schema scheming_datasets
```
