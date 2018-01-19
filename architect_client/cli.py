#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inventory script to get the metadata from the Architect service.
"""

import os
import json
import yaml
import click
from architect_client.libarchitect import ArchitectClient


def load_yaml_file(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def write_json_file(path, content):
    file_handler = open(path, "w")
    json.dump(content, file_handler)
    file_handler.close()


@click.command()
@click.option('--list', is_flag=True)
def adapter_ansible_inventory(list):
    config = load_yaml_file('/etc/architect/client.yml')
    inventory_api_url = 'http://{}:{}'.format(config['host'],
                                              config['port'])
    inventory_name = config['project']
    client = ArchitectClient(inventory_api_url, inventory_name)
    data = client.get_data('ansible-inventory')
    print(yaml.safe_dump(data))


@click.command()
@click.argument('resource_name')
def adapter_puppet_classifier(resource_name):
    config = load_yaml_file('/etc/architect/client.yml')
    inventory_api_url = 'http://{}:{}'.format(config['host'],
                                              config['port'])
    inventory_name = config['project']
    client = ArchitectClient(inventory_api_url, inventory_name)
    data = client.get_data('puppet-classifier', resource_name)
    print(yaml.safe_dump({
        'classes': data[resource_name]['applications'],
        'parameters': data[resource_name]['parameters']
    }))


@click.command()
@click.argument('resource_name')
def adapter_salt_pillar(resource_name):
    config = load_yaml_file('/etc/architect/client.yml')
    inventory_api_url = 'http://{}:{}'.format(config['host'],
                                              config['port'])
    inventory_name = config['project']
    client = ArchitectClient(inventory_api_url, inventory_name)
    data = client.get_data('salt-pillar', resource_name)
    print(yaml.safe_dump(data[resource_name]['parameters']))


@click.command()
@click.argument('resource_name')
def adapter_chef_data(resource_name, config_file=None):
    config = load_yaml_file('/etc/architect/client.yml')
    inventory_api_url = 'http://{}:{}'.format(config['host'],
                                              config['port'])
    inventory_name = config['project']
    client = ArchitectClient(inventory_api_url, inventory_name)
    data = client.get_data('chef-data', resource_name)
    if config_file is None:
        print(json.dump(data[resource_name]['parameters']))
    else:
        write_json_file(data[resource_name]['parameters'], config_file)


@click.command()
@click.argument('resource_name')
def adapter_salt_top(resource_name):
    config = load_yaml_file('/etc/architect/client.yml')
    inventory_api_url = 'http://{}:{}'.format(config['host'],
                                              config['port'])
    inventory_name = config['project']
    client = ArchitectClient(inventory_api_url, inventory_name)
    data = client.get_data('salt-top', resource_name)
    print(yaml.safe_dump({'classes': data[resource_name]['applications']}))
