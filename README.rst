
====================
The Architect Client
====================

Client library and CLI for Architect API service.


Client Installation
===================

Following steps show how to deploy and configure Architect Client.

.. code-block:: bash

    pip install architect-client

Create configuration file ``/etc/architect/client.yml`` for client.

.. code-block:: yaml

    project: project-name
    host: architect-api
    port: 8181
    username: salt
    password: password


SaltStack Integration
---------------------

To setup architect as Salt master Pillar source, set following configuration
to your Salt master at ``/etc/salt/master.d/_master.conf`` file.

.. code-block:: yaml

    ext_pillar:
      - cmd_yaml: 'architect-salt-pillar %s'

To setup architect as Salt master Tops source, set following configuration
to your Salt master at ``/etc/salt/master.d/_master.conf`` file.

.. code-block:: yaml

    master_tops:
       ext_nodes: architect-salt-top


You can test the SaltStack Pillar by calling command:

.. code-block:: bash

    $ architect-salt-pillar {{ minion-id }}


Ansible Integration
-------------------

To setup architect as Ansible dynamic inventory source, set following
configuration to your Ansible control node.

.. code-block:: bash

    $ ansible -i architect-ansible-inventory

You can test the ansible inventory by calling command:

.. code-block:: bash

    $ architect-ansible-inventory --list


Puppet Integration
------------------

To tell Puppet Server to use an ENC, you need to set two settings:
``node_terminus`` has to be set to “exec”, and ``external_nodes`` must have
the path to the executable.

.. code-block:: bash

    [master]
      node_terminus = exec
      external_nodes = /usr/local/bin/architect-puppet-classifier


Chef Integration
----------------

We can use ``-j`` parameter of ``chef-client`` command, It's the path to a
file that contains JSON data used to setup the client run. We pass

.. code-block:: bash

    $ architect-chef-data {{ node_name }} {{ file_name }}.json
    $ chef-client -j {{ file_name }}.json --environment _default


Client Usage
============

You can use the client to initialise the inventories.

.. code-block:: bash

    $ architect-inventory-create <cluster-name> <cluster-domain>

You can use the client to initialise the SaltStack managers.

.. code-block:: bash

    $ architect-manager-salt-create <manager-name> <manager-url> <manager-username> <manager-password>


References
==========

* https://docs.saltstack.com/en/latest/ref/tops/all/salt.tops.ext_nodes.html
* https://docs.saltstack.com/en/latest/ref/pillar/all/salt.pillar.cmd_yaml.html#module-salt.pillar.cmd_yaml
* http://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html
* https://puppet.com/docs/puppet/5.3/nodes_external.html
* https://docs.chef.io/ctl_chef_client.html