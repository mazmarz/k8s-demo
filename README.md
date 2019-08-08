# Purpose: 

To automate the creation of a kubernetes cluster, using kubeadm, so as to be able to run a small demo of ingress controllers and autoscaling inside K8s.  The tools used to accomplish this are:

  * Vagrant:  Used to create the VM's, spin them up and launch initially provisioning
  * Ansible:  Used to do the provisioning itself; inside Vagrant itself and separately afterwards
  * Python script:  Used to "paste" all the pieces together and to run tests at the end
  
  


There was an attempt to avoid cloud provider specific choices.  Specifically, I wanted to avoid writing the setup in a cloud specific SDK or API.  The use of vagrant and   There certainly are more clever ways to do this and hopefully, in my spare time, I will have time
to update this in the future.

Unfortunately at the moment, the number of nodes and names of the nodes has been hardcoded (master, worker1 and worker2).  With a little effort this can be changed in a newer version.
  
  
# Requirements #
  
The following is a list of software required to run this demo:

  * Vagrant.  And with vagrant one needs to install the vagrant-google plugin and that of ansible.  For the vagrant-google plugin, gcc needs to be installed
  * Ansible
  * Google's SDK, gcloud
  * The *ab* tool from apache for benchmarking
  
  
# Steps: #


The following are the macro steps I need to be done in order to run this demo. 

  
  * Log into the cloud environment and download the service-account key file which will allow you to work with the environment.  Place this file in the base directory of the demo.  The *runnit.py* script will find it.  If the are more than one of these files, it will use the latest version.
  * The script will do automatically the following:
* Setup ssh keys in order to access the cluster remotely.  With GCP this can be accomplished with gcloud compute config-ssh.  Vagrant usually handles this on its own, but needs this with GCP.
* Spin up the virtual machines.  As mentioned, I have chosen Vagrant since I am familiar with it and because it is not provider specific.
* Setup the Kubernetes inside on the VMs.  Here the choice went to Ansible.  First and foremost because it is agentless.  Though vagrant offers a provisioning method, a good part of the setup with ansible I had to do outside of vagrant.
* Apply all manifests required for this specific demo.  Again with the help of Ansible this was rather straight forward.  When possible I utilized non static manifests (from the internet).  The exception to this was the metric manifest which has a known bug and hence I found it easier to work with a modified manifest which is included in this repository.
* Setup a tcp load balancer in GCP.  Of course a static public IP is required and once this is created the nginx service manifest is patched with this address.


* The *runnit.py* script all common commands from vagrant.  For example, to log into the master node, simply type *runnit.py ssh master*.  To bring down the cluster, *runnity.py destroy -f*.
    
  
# How to run demo

 **Initial Setup:**
 
 
  * Clone the git repository onto your local machine.
  * Retrieve the json key file for the service account and place it into to the root directory
  * There script "runnit.py" is used to tie everything together.  It acts a wrapper for vagrant, hence it accepts all the common vagrant arguments: *up, down, ssh, destroy*
  * Issue the command: *runnit up*.  This should bring up the cluster and set up the load-balancer.  The static IP will be printed to the screen (along with a lot of other information) and can be used to update an /etc/hosts file.
  * Once everything is up, including the load balancer, one can run the simple demo.  The demo assumes the local installation of the "ab" program from apache.org.  
  
  
