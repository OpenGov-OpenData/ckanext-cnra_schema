#!/usr/bin/env/python
from setuptools import setup

setup(
    name='ckanext-cnra_schema',
    version='0.1',
    description='',
    license='AGPL3',
    author='Jay Guo',
    author_email='jguo@opengov.com',
    url='',
    namespace_packages=['ckanext'],
    packages=['ckanext.cnra_schema'],
    zip_safe=False,
    entry_points = """
        [ckan.plugins]
        cnra_schema = ckanext.cnra_schema.plugins:cnraSchema
    """
)
