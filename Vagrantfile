# require 'getoptlong'

# opts = GetoptLong.new(
#   [ '--credentials' , GetoptLong::OPTIONAL_ARGUMENT ],
#   [ '--project_id', GetoptLong::OPTIONAL_ARGUMENT ]
# )

projectID=ENV['PROJECT_ID']
credentials=ENV['CREDENTIALS']
# user=%x[whoami].chomp()
user=ENV['USER']


# opts.each do |opt, arg|
#   case opt
#     when '--project_id'
#       projectID=arg
#     when '--credentials'
#       credentials=arg
#   end
# end


#credentials = 'playground-s-11-e49d28-07e7f0721a24.json'
#projectID = 'playground-s-11-e49d28'

nodes = [
  {ID: 1,  hostname: 'master', box: 'mgmazzucco/CentOS7_ESX', role: 'master' },
  {ID: 2,  hostname: 'worker1', box: 'mgmazzucco/CentOS7_ESX' , role: 'worker' },
  {ID: 3,  hostname: 'worker2', box: 'mgmazzucco/CentOS7_ESX' , role: 'worker' }
]



Vagrant.configure("2") do |config|


  
  config.vm.box = "google/gce"
  config.vm.synced_folder '.', '/vagrant', disabled: true

  config.vm.provision :ansible  do |ansible|
    ansible.groups = {
      "workers" => ["worker1","worker2"],
      "master" => ["master"]
    }
    ansible.playbook = "k8s_playbook.yaml"
    
  end
  # config.vm.provision :ansible, preserve_order: true do |ansible|
  #   ansible.playbook = "master_playbook.yaml"
  #   puts "master"
    
  # end
  
  nodes.each do |node|

    config.vm.define node[:hostname] do |hostname|

      
      
      hostname.vm.provider :google do |google, override|
        google.google_project_id = projectID
        google.google_json_key_location = "/home/marco/puppet/#{credentials}"
        google.image_family = 'rhel-7'
        google.machine_type = 'g1-small'
        google.instance_group = 'vm-pool'
        google.name = node[:hostname]
        override.ssh.username = user
        override.ssh.private_key_path = "~/.ssh/google_compute_engine"
      end

    end
      
  end

end
    
  

