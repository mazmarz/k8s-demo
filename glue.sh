#!/bin/bash

vagrant up


env ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook cluster_playbook.yaml -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --private-key=~/.ssh/id_rsa -u marco
