#!/usr/bin/env python3

import subprocess
import sys
import re
import json
import argparse

parser = argparse.ArgumentParser(description='Setup K8s environment and run some tests')


listing = subprocess.getoutput('ls -rt')

for file in listing.splitlines():
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
            subprocess.check_call(['gcloud',"auth","activate-service-account","--key-file={}".format(theFile)] )
            subprocess.check_call(['gcloud',"config","set","project",data['project_id'] ])
        except subprocess.CalledProcessError:
            sys.exit(-2)

        try:
            subprocess.check_call(['gcloud',"compute","config-ssh"] )
        except subprocess.CalledProcessError:
            sys.exit(-2)
                          
                
        try:
            subprocess.check_call(['vagrant',"--project_id={}".format(data['project_id']),"--credentials={}".format(theFile),'up'])
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
        try:
            print("### Setting up the metric controller")
            subprocess.Popen(["ansible-playbook", "metric_playbook.yaml", "-i", ".vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory", "--private-key=~/.ssh/id_rsa", "-u" ," marco"], env={"ANSIBLE_HOST_KEY_CHECKING": "False"}).wait()
        except subprocess.CalledProcessError:
            sys.exit(-2)
        try:
            print("### Setting up the guestbook")
            subprocess.Popen(["ansible-playbook", "guestbook_playbook.yaml", "-i", ".vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory", "--private-key=~/.ssh/id_rsa", "-u" ," marco"], env={"ANSIBLE_HOST_KEY_CHECKING": "False"}).wait()
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
            subprocess.check_call(['vagrant',"--project_id={}".format(data['project_id']),"--credentials={}".format(theFile),'destroy','--force'] )
        except subprocess.CalledProcessError:
            sys.exit(-2)

    elif vagrantCommand == "test":
        try:
            subprocess.getoutput(['ssh','-i','~/.ssh/id_rsa.pub','kubectl get hpa -A'])
        except subprocess.CalledProcessError:
            sys.exit(-2)


    else:
        print(vagrantCommand + " is not a valid vagrant option or the key word \'test\' ")

else:
    print("I need an argument ...  ")
        

    

#    gcloud compute instance-groups unmanaged create k8s --zone us-central1-f
#    gcloud compute instance-groups set-named-ports  k8s --named-ports tcp80:80 --zone us-central1-f 
#    gcloud compute instance-groups unmanaged add-instances k8s --instances master,worker1,worker2 --zone us-central1-f
#    gcloud compute health-checks create  tcp my-health --port 80     
#    gcloud compute backend-services create lb --global --protocol TCP --port-name tcp80 --health-checks my-health
#    gcloud compute target-tcp-proxies create my-tcp-lb-target-proxy --backend-service lb --proxy-header NONE
# gcloud compute addresses list
# gcloud compute backend-services create lb-regional  --protocol TCP --port-name tcp80 --health-checks my-health --region us-central1 --load-balancing-scheme INTERNAL


#     gcloud compute target-pools add-instances www-pool  --instances www1,www2,www3   --instances-zone us-central1-b
# gcloud compute addresses create network-lb-ip-1     --region us-central1
# gcloud compute forwarding-rules create www-rule     --region us-central1     --ports 80     --address network-lb-ip-1     --target-pool www-pool
