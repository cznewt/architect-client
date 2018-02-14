#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inventory script to get the metadata from the Architect service.
"""

import json
import yaml
import click
from architect_client.libarchitect import ArchitectClient, write_json_file


@click.command()
@click.argument('cluster_name')
@click.argument('domain_name')
def client_inventory_create(cluster_name, domain_name):
    client = ArchitectClient()
    data = client.create_inventory(cluster_name, domain_name)
    print(yaml.safe_dump(data))


@click.command()
@click.argument('manager_name')
@click.argument('manager_url')
@click.argument('manager_user')
@click.argument('manager_password')
def client_manager_salt_create(manager_name, manager_url,
                               manager_user, manager_password):
    client = ArchitectClient()
    data = client.create_manager(manager_name, manager_url,
                                 manager_user, manager_password)
    print(yaml.safe_dump(data))


@click.command()
@click.option('--list', is_flag=True)
def adapter_ansible_inventory(list):
    client = ArchitectClient()
    data = client.get_data('ansible-inventory')
    print(yaml.safe_dump(data))


@click.command()
@click.argument('resource_name')
def adapter_puppet_classifier(resource_name):
    client = ArchitectClient()
    data = client.get_data('puppet-classifier', resource_name)
    print(yaml.safe_dump({
        'classes': data[resource_name]['applications'],
        'parameters': data[resource_name]['parameters']
    }))


@click.command()
@click.argument('resource_name')
def adapter_salt_pillar(resource_name):
    client = ArchitectClient()
    data = client.get_data('salt-pillar', resource_name)
    print(yaml.safe_dump(data[resource_name]['parameters']))


@click.command()
@click.argument('resource_name')
def adapter_chef_data(resource_name, config_file=None):
    client = ArchitectClient()
    data = client.get_data('chef-data', resource_name)
    if config_file is None:
        print(json.dump(data[resource_name]['parameters']))
    else:
        write_json_file(data[resource_name]['parameters'], config_file)


@click.command()
@click.argument('resource_name')
def adapter_salt_top(resource_name):
    client = ArchitectClient()
    data = client.get_data('salt-top', resource_name)
    print(yaml.safe_dump({'classes': data[resource_name]['applications']}))
