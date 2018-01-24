# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = '0.5'

with open('README.rst') as readme:
    LONG_DESCRIPTION = ''.join(readme.readlines())

DESCRIPTION = """Architect Client is client-side of service modeling,
management and visualization platform."""

setup(
    name='architect-client',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Aleš Komárek',
    author_email='ales.komarek@newt.cz',
    license='Apache License, Version 2.0',
    url='https://github.com/cznewt/architect-client/',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'requests',
        'Click',
    ],
    classifiers=[
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'architect-ansible-inventory = architect_client.cli:adapter_ansible_inventory',
            'architect-chef-data = architect_client.cli:adapter_chef_data',
            'architect-puppet-classifier = architect_client.cli:adapter_puppet_classifier',
            'architect-salt-pillar = architect_client.cli:adapter_salt_pillar',
            'architect-salt-top = architect_client.cli:adapter_salt_top',
        ],
    },
)
