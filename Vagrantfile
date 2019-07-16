nodes = [
  {ID: 1,  hostname: 'master', box: 'mgmazzucco/CentOS7_ESX', role: 'master' },
  {ID: 2,  hostname: 'worker1', box: 'mgmazzucco/CentOS7_ESX' , role: 'worker' },
  {ID: 3,  hostname: 'worker2', box: 'mgmazzucco/CentOS7_ESX' , role: 'worker' }
]



Vagrant.configure("2") do |config|


  
  config.vm.box = "google/gce"
  config.vm.synced_folder '.', '/vagrant', disabled: true

  config.vm.provision :ansible , preserve_order: true do |ansible|
    ansible.playbook = "k8s_playbook.yaml"
    puts "all"
    
  end
  config.vm.provision :ansible, preserve_order: true do |ansible|
    ansible.playbook = "master_playbook.yaml"
    puts "master"
    
  end
  
  
  nodes.each do |node|

    config.vm.define node[:hostname] do |hostname|

      
      
      hostname.vm.provider :google do |google, override|
        google.google_project_id = "playground-s-11-d19c7b"
        google.google_json_key_location = "/home/marco/puppet/playground-s-11-d19c7b-bf020550a8a7.json"
        google.image_family = 'rhel-7'
        google.name = node[:hostname]
        override.ssh.username = "marco"
        override.ssh.private_key_path = "~/.ssh/id_rsa"
      end

    end
      
  end

  
    


    
  
end
