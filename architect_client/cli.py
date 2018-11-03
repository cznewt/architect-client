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
        'classes': data.get(resource_name, {}).get('applications', {}),
        'parameters': data.get(resource_name, {}).get('parameters', {})
    }))


@click.command()
@click.argument('resource_name')
def adapter_salt_pillar(resource_name):
    client = ArchitectClient()
    data = client.get_data('salt-pillar', resource_name)
    print(yaml.safe_dump(data.get(resource_name, {}).get('parameters', {})))


@click.command()
@click.argument('resource_name')
def adapter_chef_data(resource_name, config_file=None):
    client = ArchitectClient()
    data = client.get_data('chef-data', resource_name)
    if config_file is None:
        print(json.dumps(data.get(resource_name, {}).get('parameters', {})))
    else:
        write_json_file(data.get(resource_name, {}).get('parameters', {}), config_file)


@click.command()
@click.argument('resource_name')
def adapter_salt_top(resource_name):
    client = ArchitectClient()
    response = client.get_data('salt-top', resource_name)
    data = response.get(resource_name, {}).get('applications', [])
    if client.salt_top_prepend_host:
        new_data = []
        for datum in data:
            new_data.append(resource_name + '.' + datum)
        data = new_data
    print(yaml.safe_dump({'classes': data}))
