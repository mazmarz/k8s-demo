credentials = 'playground-s-11-e3bd2e-4124c19ed7c2.json'
projectID = 'playground-s-11-e3bd2e'

nodes = [
  {ID: 1,  hostname: 'master', box: 'mgmazzucco/CentOS7_ESX', role: 'master' },
  {ID: 2,  hostname: 'worker1', box: 'mgmazzucco/CentOS7_ESX' , role: 'worker' },
  {ID: 3,  hostname: 'worker2', box: 'mgmazzucco/CentOS7_ESX' , role: 'worker' }
]



Vagrant.configure("2") do |config|


  
  config.vm.box = "google/gce"
  config.vm.synced_folder '.', '/vagrant', disabled: true

  config.vm.provision :ansible , preserve_order: true do |ansible|
    ansible.groups = {
      "workers" => ["worker1","worker2"],
      "master" => ["master"]
    }
    ansible.playbook = "k8s_playbook.yaml"
    puts "all"
    
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
        google.name = node[:hostname]
        override.ssh.username = "marco"
        override.ssh.private_key_path = "~/.ssh/id_rsa"
      end

    end
      
  end

end
    
  

