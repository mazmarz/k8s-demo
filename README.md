# Purpose: 

To automate the creation of a kubernetes cluster, using kubeadm, so as to be able to run a small demo of ingress controllers and autoscaling inside K8s.  The tools used to accomplish this are:

  * Vagrant:  Used to create the VM's, spin them up and launch initially provisioning
  * Ansible:  Used to do the provisioning itself; inside Vagrant itself and separately afterwards
  * Python script:  Used to "paste" all the pieces together and to run tests at the end
  
  


There was an attempt to avoid cloud provider specific choices use of vagrant and ansible.   There certainly are more clever ways to do this and hopefully, in my spare time, I will have time
to update this in the future.

Unfortunately at the moment, the number of nodes and names of the nodes has been hardcoded (master, worker1 and worker2).  With a little effort this can be changed in a newer version.
  
  
# Requirements #
  
The following is a list of software required to run this demo:

  * Vagrant.  And with vagrant one needs to install the vagrant-google plugin and that of ansible.  For the vagrant-google plugin, gcc needs to be installed
  * Ansible
  * Google's SDK, gcloud
  * The *ab* tool from apache for benchmarking
  
  
# Steps: #


The following are the macro steps which need to be done in order to run this demo. 

  
  * Retrieve the json key file for the service account and place it into to the root directory 
  * The script will do automatically the following:
    - Setup ssh keys in order to access the cluster remotely.  With GCP this can be accomplished with gcloud compute config-ssh.  Vagrant can handle this on its own but not with GCP it seems.
    - Spin up the virtual machines.  As mentioned, I have chosen Vagrant since I am familiar with it and because it is not provider specific.
    - Setup the Kubernetes inside on the VMs.  Here the choice went to Ansible.  First and foremost because it is agentless.  Though vagrant offers a provisioning method, a good part of the setup with ansible I had to do outside of vagrant.
    - Apply all manifests required for this specific demo.  Again with the help of Ansible this was rather straight forward.  When possible I utilized non static manifests (from the internet).  The exception to this was the metric manifest which has a known bug and hence I found it easier to work with a modified manifest which is included in this repository.
    - Setup a tcp load balancer in GCP.  Of course a static public IP is required and once this is created the nginx service manifest is patched with this address.


* The *runnit* script all common commands from vagrant.  For example, to log into the master node, simply type `runnit ssh master`.  To bring down the cluster, `runnity.py destroy -f`.
    
  
# How to run demo

 **Initial Setup:**
 
 
  * Clone the git repository onto your local machine.
  * Log into the cloud environment and download the service-account key file which will allow you to work with the environment.  Place this file in the base directory of the demo.  The *runnit* script will find it.  If the are more than one of these files, it will use the latest version.
  * There script *runnit* is used to tie everything together.  It acts a wrapper for vagrant, hence it accepts all the common vagrant arguments: *up, down, ssh, destroy*
  * Issue the command: `runnit up`.  This should bring up the cluster and set up the load-balancer.  The static IP will be printed to the screen (along with a lot of other information, to be cleaned up in the future) and can be used to update an /etc/hosts file.
  
  **Running demo**
  
  Once everything is up, hopefully without errors (if there is an error, try doing a *runnit destroy -f* followed by a *runnit up*), you can try a `runnit test`.  This will setup a monitoring horizontal pod autoscaler on the two namespaces of the demo. **One needs to wait till the number of pods goes down to 1 before starting the test.**  This is because it takes time for the metric controller to settle and the hpa controller to react.  Once this state has been achieved, from another terminal one can launch: `ab -c 1000 -n 20000 http://stagging-guestbook.mstakx.io/` and/or `ab -c 1000 -n 20000 http://guestbook.mstakx.io/`
  
  
