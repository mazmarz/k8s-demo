# Purpose: 

To automate the creation of a kubernetes cluster so as to be able to run a small demo of ingress controllers and autoscaling inside K8s.  The tools used to accomplish this are:

  * Vagrant:  Used to create the VM's, spin them up and launch initially provisioning
  * Ansible:  Used to do the provisioning itself; inside Vagrant itself and separately afterwards
  * Python script:  Used to "paste" all the pieces together and to run tests at the end
  
  


There was an attempt, as much as possible, to avoid cloud provider specific choices.  Specifically, I wanted to avoid writing the setup in a cloud specific SDK or API. A decent portion of what was written here 
can be easily adapted to another cloud provider or even home lab virtualization environment.  There certainly are more clever ways to do this and hopefully, in my spare time, I will have time
to update this in the future.
  
  
# Steps: #


The following are the macro steps I need to be done in order to run this demo. 

  
  * Log into the cloud environment and get some sort of key to allow working with the environment.  In the case of GCP: glcoud auth activate-service-account.
  * Setup ssh keys in order to access the cluster remotely.  With GCP this can be accomplished with gcloud compute config-ssh.  Vagrant usually handles this on its own, but needs this with GCP.
  * Spin up the virtual machines.  As mentioned, I have chosen Vagrant since I have used it in the past in more than one occasion and because it is not provider specific
  * Setup the Kubernetes inside on the VMs.  Here the choice went to Ansible.  First and foremost because it is agentless.  Though vagrant offers a provisioning method, part of the setup I had to do outside
  of vagrant since I seems there is no way to apply a ansible playbook on a group of machines but only on a single VM at a time.
  * Apply all manifests required for this specific demo.  Again with the help of Ansible this was rather straight forward.  When possible I utilized non static manifests (from the internet).  The exception to this was the metric manifest which has a known bug and hence I found it easier to work with a modified manifest which is included in this repository.
  * For now, I have NOT automated the setup of the required load balancer.  This can be done in several steps with the SDK but I found this tedious and this will certainly be quite different for every cloud provider.  I will attempt to a more "elegant" solution to this issue in the coming 
  
  
  
# How to run demo

 **Initial Setup:**
 
 
  * Clone the git repository onto your local machine a log into the GCP platform. 
  * Retrieve the json key file for the service account and place it into to the root directory
  * Place your ssh pub key into the public account.  Currently vagrant expects the current user (whoami) and the pub key file: google_compute_engine.pub inside ~/.ssh/
  * There script "runnit.py" is used to tie everything together.  It acts a wrapper for vagrant, hence it accepts all the common vagrant arguments: *up, down, ssh, destroy*
  * Currently I have "hardcoded" a specific configuration with one master and two works with names: worker1 and worker2.  This is easily changed, but I haven't done it yet.
  * After running *runnit up*, the environment is ready to go EXCEPT for the load balancer.  As mentioned earlier, for now, this remains the only "manual" part.  Also, I assume the firewall inside GCP has been open for the demo.fLyMd-mAkEr
  * Once everything is up, including the load balancer, one can run the simple demo.  The demo assumes the local installation of the "ab" program from apache.org.  
  
  
