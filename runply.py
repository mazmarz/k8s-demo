#!/usr/bin/env python3

import subprocess, sys
import re
import json

try:
    subprocess.Popen("/usr/bin/env ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook cluster_playbook.yaml -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --private-key=~/.ssh/id_rsa -u marco", shell=True )
#    subprocess.check_call(["/usr/bin/env", "ANSIBLE_HOST_KEY_CHECKING=False"])

except subprocess.CalledProcessError:
    sys.exit(-2)


    

    
