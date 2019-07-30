#!/usr/bin/env python3

import subprocess
import sys
import re
import json



listing = subprocess.getoutput('ls -rt')

for file in listing.split():
    if re.match('.*\.json$',file):
        theFile = file


with  open(theFile) as json_file:
    data = json.load(json_file)
print(data['project_id'])

if len(sys.argv) > 1:

    vagrantCommand = sys.argv[1]

    if vagrantCommand == "ssh":
        if len(sys.argv) > 2:
            machine = sys.argv[2]
        else:
            machine = ""
        try:
            subprocess.check_call(['vagrant',"--project_id={}".format(data['project_id']),"--credentials={}".format(theFile),'ssh',machine] )
        except subprocess.CalledProcessError:
            sys.exit(-2)

    elif vagrantCommand == "up":
        try:
            subprocess.check_call(['vagrant',"--project_id={}".format(data['project_id']),"--credentials={}".format(theFile),'up'] )
        except subprocess.CalledProcessError:
            sys.exit(-2)
        try:
            print("#### Setting up the K8s cluster")
            subprocess.Popen(["ansible-playbook", "cluster_playbook.yaml", "-i", ".vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory", "--private-key=~/.ssh/id_rsa", "-u" ," marco"], env={"ANSIBLE_HOST_KEY_CHECKING": "False"}).wait()
        except subprocess.CalledProcessError:
            sys.exit(-2)
        try:
            print("### Setting up the Ingress controller")
            subprocess.Popen(["ansible-playbook", "ingress_playbook.yaml", "-i", ".vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory", "--private-key=~/.ssh/id_rsa", "-u" ," marco"], env={"ANSIBLE_HOST_KEY_CHECKING": "False"}).wait()
        except subprocess.CalledProcessError:
            sys.exit(-2)


    elif vagrantCommand == "status":
        try:
            subprocess.check_call(['vagrant',"--project_id={}".format(data['project_id']),"--credentials={}".format(theFile),'status'] )
        except subprocess.CalledProcessError:
            sys.exit(-2)

    elif vagrantCommand == "halt":
        try:
            subprocess.check_call(['vagrant',"--project_id={}".format(data['project_id']),"--credentials={}".format(theFile),'halt'] )
        except subprocess.CalledProcessError:
            sys.exit(-2)

    elif vagrantCommand == "destroy":
        try:
            subprocess.check_call(['vagrant',"--project_id={}".format(data['project_id']),"--credentials={}".format(theFile),'destroy'] )
        except subprocess.CalledProcessError:
            sys.exit(-2)

    else:
        print("vagrant command:" + vagrantCommand + " not found")

else:
    print("I need an argument ...")
        

    


    

    
