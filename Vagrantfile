# -*- mode: ruby -*-
# vi: set ft=ruby :

# WARNING: This file works only with virtualbox provider!!!

Vagrant.configure("2") do |config|
  # config.vm.box_check_update = false
    
  ####################################################[ROUTER]##################################################################

  config.vm.define "router" do |router|
    router.vm.box = "Dealmi/ubuntu20_elk_agent" #ELK Included and fleet server is up and running
    # router.vm.box_version = "1.0.1"
    router.vm.hostname = "router"
    router.vm.provider "virtualbox" do |vb|
      vb.memory = "6144"
      vb.cpus = "3"
    end
  
       
    # intranet 1
    router.vm.network "private_network", auto_config: false, virtualbox__intnet: "net1"
    # intranet 2
    router.vm.network "private_network", auto_config: false, virtualbox__intnet: "net2"
       
    # Kibana port forwarding
    router.vm.network "forwarded_port", guest: 5601, host: 5601

    router.vm.provision "file", source: "router/50-vagrant.yaml", destination: "~/50-vagrant.yaml"
   
    router.vm.provision "shell", inline: <<-SHELL
      sudo chown root.root 50-vagrant.yaml && sudo chmod 644 50-vagrant.yaml
      sudo mv -f /home/vagrant/50-vagrant.yaml  /etc/netplan
      sudo netplan apply
    SHELL

    router.vm.provision "shell", inline: <<-SHELL
      # Updating the system
      sudo timedatectl set-timezone Europe/Moscow
      sudo apt remove multipath-tools -y  #we don't have devices for this daemon and it just spams in log-files
      sudo apt remove ufw -y #we gonna use standart iptables rules management
      sudo mv /etc/apt/sources.list.d/elastic-7.x.list /home/vagrant #turning off ELK update
      sudo apt-get update
      sudo apt-get full-upgrade -y
      # installing DHCP server
      sudo apt-get install -y isc-dhcp-server
      # installing DNS server
      sudo apt-get install -y bind9
      # Enabling routing
      sudo echo \"net.ipv4.ip_forward=1\" >> /etc/sysctl.conf
      sudo sysctl -p  
      
    SHELL
    # Setting up DNS server
    router.vm.provision "file", source: "router/db.10.0.10", destination: "~/db.10.0.10"
    router.vm.provision "file", source: "router/db.20.0.10", destination: "~/db.20.0.10"
    router.vm.provision "file", source: "router/db.service", destination: "~/db.service"
    router.vm.provision "file", source: "router/named.conf.local", destination: "~/named.conf.local"
    # router.vm.provision "file", source: "router/named.conf", destination: "~/named.conf"
    router.vm.provision "file", source: "router/named.conf.options", destination: "~/named.conf.options"
    router.vm.provision "shell", inline: <<-SHELL
      sudo chown bind.bind /home/vagrant/db*
      sudo chown root.bind /home/vagrant/named*
      sudo chmod 644 /home/vagrant/db*
      sudo chmod 664 /home/vagrant/named*
      sudo mv -f /home/vagrant/named.* /etc/bind
      sudo mv /home/vagrant/db* /var/lib/bind/
      sudo systemctl restart named
    SHELL
    # Setting up DHCP server
    router.vm.provision "file", source: "router/isc-dhcp-server", destination: "~/isc-dhcp-server"
    router.vm.provision "file", source: "router/dhcpd.conf", destination: "~/dhcpd.conf"
    router.vm.provision "shell", inline: <<-SHELL
      sudo chown root.root /home/vagrant/*dhcp*
      sudo chmod 644 /home/vagrant/*dhcp*
      sudo mv -f /home/vagrant/isc-dhcp-server /etc/default
      sudo mv -f /home/vagrant/dhcpd.conf /etc/dhcp
      sudo cp /etc/bind/rndc.key /etc/dhcp/
      sudo systemctl disable isc-dhcp-server6
      sudo systemctl restart isc-dhcp-server
    SHELL

    #Installing wireshark
    router.vm.provision "shell", inline: "sudo DEBIAN_FRONTEND=noninteractive apt-get install termshark -y"
    
    #Adding rsyslogd config for iptables
    router.vm.provision "file", source: "router/19-iptables.conf", destination: "/home/vagrant/19-iptables.conf"
    router.vm.provision "shell", inline: <<-SHELL
      sudo chmod 644 /home/vagrant/19-iptables.conf 
      sudo chown root.root /home/vagrant/19-iptables.conf
      sudo mv -f /home/vagrant/19-iptables.conf  /etc/rsyslog.d
    SHELL

    #Adding iptables logfile rotation
    router.vm.provision "file", source: "router/iptables", destination: "/home/vagrant/iptables"
    router.vm.provision "shell", inline: <<-SHELL
      sudo chmod 644 /home/vagrant/iptables 
      sudo chown root.root /home/vagrant/iptables 
      sudo mv -f /home/vagrant/iptables /etc/logrotate.d/
    SHELL
    #IP-tables saver
    router.vm.provision "shell", inline: "sudo DEBIAN_FRONTEND=noninteractive apt-get install iptables-persistent -y"
    #IP-tables rules
    router.vm.provision "file", source: "router/rules.v4", destination: "/home/vagrant/rules.v4"
    router.vm.provision "file", source: "router/rules.fix", destination: "/home/vagrant/rules.fix"
    router.vm.provision "shell", inline: <<-SHELL
      sudo chmod 644 /home/vagrant/rules.* 
      sudo chown root.root /home/vagrant/rules.* 
      sudo mv -f /home/vagrant/rules.* /etc/iptables
    SHELL
     #Apply firewall rules and reboot
     router.vm.provision "shell", inline: "sudo iptables-restore /etc/iptables/rules.fix" #We need this to keep connection alive between vagrant and guest
     router.vm.provision "shell", inline: "sudo iptables-restore /etc/iptables/rules.v4", reboot: true
  end
    
  ####################################################[DATA]#########################################################################
  
  config.vm.define "data" do |data|
    data.vm.box = "ubuntu/focal64"  
    data.vm.hostname = "data"
    data.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = "1"
    end
   # intranet 2
    data.vm.network "private_network", auto_config: false, virtualbox__intnet: "net2"
  
    #Adding a routing
    data.vm.provision "file", source: "data/50-vagrant.yaml", destination: "~/50-vagrant.yaml"
    data.vm.provision "shell", inline: <<-SHELL
      sudo chown root.root 50-vagrant.yaml && sudo chmod 644 50-vagrant.yaml
      sudo mv -f /home/vagrant/50-vagrant.yaml  /etc/netplan
      sudo netplan apply
    SHELL
    # MySQL port forwarding
    data.vm.network "forwarded_port", guest: 3306, host: 3306
    
    # Extra disks for lvm and mdraid
    data.vm.disk :disk, name: "lvm_files1", size: "512MB"
    data.vm.disk :disk, name: "lvm_files2", size: "512MB"
    data.vm.disk :disk, name: "mdraid_backup1", size: "1GB"
    data.vm.disk :disk, name: "mdraid_backup2", size: "1GB"
    
    # LVM 
    data.vm.provision "shell", inline: <<-SHELL
      sudo pvcreate /dev/sdc /dev/sdd
      sudo vgcreate lvm_files /dev/sdc /dev/sdd
      sudo lvcreate -m1 -l100%VG --type raid1 -Ay --monitor y -n LV_files lvm_files
      sudo mkfs.xfs /dev/lvm_files/LV_files
      sudo mkdir -p /local/files
      sudo mount /dev/lvm_files/LV_files /local/files/
      cat /etc/mtab | grep "lvm_files" | sudo tee -a /etc/fstab
    SHELL

    # RAID-1 (mdraid) for backups
    data.vm.provision "shell", inline: <<-SHELL
      yes | sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sde /dev/sdf
      sudo mkfs.xfs /dev/md0
      sudo mkdir /local/backups
      sudo mount /dev/md0 /local/backups/
      cat /etc/mtab | grep md0 | sudo tee -a /etc/fstab
    SHELL
        
    # System update
    data.vm.provision "shell", inline: <<-SHELL
      sudo timedatectl set-timezone Europe/Moscow
      sudo apt remove multipath-tools -y  #we don't have devices for this daemon and it just spams in log-files
      sudo apt remove ufw -y #we gonna use standart iptables rules management
      sudo apt-get update
      sudo apt-get full-upgrade -y
      

     # Installing MySQL server
      sudo apt install -y mysql-server
    SHELL
    #Installing mail tools
    data.vm.provision "shell", inline:"sudo DEBIAN_FRONTEND=noninteractive apt install mailutils -y"

   # MySQL
   data.vm.provision "file", source: "data/mysqld.cnf", destination: "~/mysqld.cnf"
   data.vm.provision "shell", inline: <<-SHELL
      sudo mkdir /local/files/mysql
      sudo mv -f /home/vagrant/mysqld.cnf /etc/mysql/mysql.conf.d/
      sudo chown root.root /etc/mysql/mysql.conf.d/mysqld.cnf
      sudo systemctl restart mysql
   SHELL
   #Creating data for web app
   data.vm.provision "file", source: "data/mysql.sql", destination: "~/mysql.sql"
   data.vm.provision "file", source: "data/webapp.sql", destination: "~/webapp.sql"
   data.vm.provision "shell", inline: <<-SHELL
     sudo mysql mysql < mysql.sql
     sudo mysql -e "flush privileges"
     sudo mysql -e "create database webapp" && sudo mysql webapp < webapp.sql
     rm -f *.sql 
   SHELL

   # Cleaning unused packets
   data.vm.provision "shell", inline: "sudo apt-get clean -y && sudo apt-get autoremove -y"
  
    # Installing bash scripts from the task:
    # First
    data.vm.provision "file", source: "data/dataRead.sh", destination: "~/dataRead.sh"
    # Second
    data.vm.provision "file", source: "data/service_scripts/backup.sh", destination: "~/backup.sh"
    data.vm.provision "file", source: "data/service_scripts/backup.service", destination: "~/backup.service"
    data.vm.provision "file", source: "data/service_scripts/backup.conf", destination: "~/backup.conf"
    data.vm.provision "shell", inline: <<-SHELL
     sudo chmod +x /home/vagrant/*.sh
     sudo mkdir /usr/lib/backup
     sudo mv -f /home/vagrant/backup.sh /usr/lib/backup/
     sudo mv -f /home/vagrant/backup.service /etc/systemd/system
     sudo mv -f /home/vagrant/backup.conf /etc/ 
     sudo systemctl start backup
   SHELL

    #Elastic-agent 
    data.vm.provision "shell", inline: <<-SHELL
     wget -q https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-7.15.2-linux-x86_64.tar.gz
     tar -xzf elastic-agent-7.15.2-linux-x86_64.tar.gz
     sudo /home/vagrant/elastic-agent-7.15.2-linux-x86_64/elastic-agent install -f --url=https://router:8220 --enrollment-token=SVo1OGpIMEJIamFMRU9CeUN4Ujc6bGFJNGhPUW9STTJzVU1USEFMc0x3QQ== --insecure
    SHELL

    #IP-tables saver
    data.vm.provision "shell", inline: "sudo DEBIAN_FRONTEND=noninteractive apt-get install iptables-persistent -y"
    #IP-tables rules
    data.vm.provision "file", source: "data/rules.v4", destination: "/home/vagrant/rules.v4"
    data.vm.provision "file", source: "data/rules.fix", destination: "/home/vagrant/rules.fix"
    data.vm.provision "shell", inline: <<-SHELL
      sudo chmod 644 /home/vagrant/rules.* 
      sudo chown root.root /home/vagrant/rules.* 
      sudo mv -f /home/vagrant/rules.* /etc/iptables
    SHELL
    #Apply firewall rules and reboot
    data.vm.provision "shell", inline: "sudo iptables-restore /etc/iptables/rules.fix" #We need this to keep connection alive between vagrant and guest
    data.vm.provision "shell", inline: "sudo iptables-restore /etc/iptables/rules.v4", reboot: true

  end

 ########################################################[WEB]##########################################################
  
  config.vm.define "web" do |web|
    web.vm.box = "ubuntu/focal64"
    web.vm.hostname = "web"
    web.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = "1"
    end
    # External network
    web.vm.network "public_network", bridge: "Realtek PCIe GbE Family Controller"
    # intranet 1
    web.vm.network "private_network", auto_config: false, virtualbox__intnet: "net1"
        
    # Adding a routing
    web.vm.provision "file", source: "web/50-vagrant.yaml", destination: "/home/vagrant/50-vagrant.yaml"
    web.vm.provision "shell", inline: <<-SHELL
      sudo chown root.root 50-vagrant.yaml && sudo chmod 644 50-vagrant.yaml
      sudo mv -f /home/vagrant/50-vagrant.yaml  /etc/netplan
      sudo netplan apply
    SHELL
   
    # Updating the system
    web.vm.provision "shell", inline: <<-SHELL
      sudo timedatectl set-timezone Europe/Moscow
      sudo apt remove multipath-tools -y  #we don't have devices for this daemon and it just spams in log-files
      sudo apt remove ufw -y #we gonna use standart iptables rules management
      sudo apt-get update
      sudo apt-get full-upgrade -y 
    SHELL
    
    # Installing pip and mysql driver for python 3
    web.vm.provision "file", source: "web/get-pip.py", destination: "~/get-pip.py"
    web.vm.provision "shell", inline: "sudo python3 /home/vagrant/get-pip.py"
    web.vm.provision "shell", inline: "sudo pip install mysql-connector-python"
    
    # Nginx
    web.vm.provision "shell", inline: "sudo apt install -y nginx"
    web.vm.provision "file", source: "web/nginx/sites-available/website.conf", destination: "~/website.conf"
    web.vm.provision "file", source: "web/nginx/sites-available/website.conf.protected", destination: "~/website.conf.protected"
    web.vm.provision "file", source: "web/nginx/ssl/webnews.crt", destination: "~/webnews.crt"
    web.vm.provision "file", source: "web/nginx/ssl/webnews.key", destination: "~/webnews.key"
    web.vm.provision "shell", inline: <<-SHELL
      sudo rm -f /etc/nginx/sites-enabled/default
      sudo mv -f /home/vagrant/website.conf /etc/nginx/sites-available/website.conf
      sudo mv -f /home/vagrant/website.conf.protected /etc/nginx/sites-available/website.conf.protected
      sudo mkdir /etc/nginx/ssl
      sudo chmod 700 /etc/nginx/ssl
      sudo mv -f /home/vagrant/webnews.crt /etc/nginx/ssl/
      sudo mv -f /home/vagrant/webnews.key /etc/nginx/ssl/
      sudo ln -s /etc/nginx/sites-available/website.conf /etc/nginx/sites-enabled/website.conf
      sudo systemctl enable nginx && sudo systemctl restart nginx
      mkdir -p /local/files && mkdir /local/scripts
    SHELL
    #Adding files to the web-server
    web.vm.provision "file", source: "web/start.html", destination: "~/start.html"
    web.vm.provision "file", source: "web/getData.py", destination: "~/getData.py"
    web.vm.provision "file", source: "web/webnews", destination: "~/webnews"
    web.vm.provision "shell", inline: <<-SHELL
      sudo mv -f /home/vagrant/start.html /local/files/
      sudo mv -f /home/vagrant/getData.py /local/scripts/
      sudo chown root.root /home/vagrant/webnews && sudo chmod 644 /home/vagrant/webnews
      sudo mv -f /home/vagrant/webnews /etc/cron.d/
      sudo systemctl restart cron
    SHELL

    # Elastic-agent
    web.vm.provision "shell", inline: <<-SHELL
      wget -q https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-7.15.2-linux-x86_64.tar.gz
      tar -xzf elastic-agent-7.15.2-linux-x86_64.tar.gz
      sudo /home/vagrant/elastic-agent-7.15.2-linux-x86_64/elastic-agent install -f --url=https://router:8220 --enrollment-token=SVo1OGpIMEJIamFMRU9CeUN4Ujc6bGFJNGhPUW9STTJzVU1USEFMc0x3QQ== --insecure
    SHELL

    #IP-tables saver
    web.vm.provision "shell", inline: "sudo DEBIAN_FRONTEND=noninteractive apt-get install iptables-persistent -y"
    #IP-tables rules
    web.vm.provision "file", source: "web/rules.v4", destination: "/home/vagrant/rules.v4"
    web.vm.provision "file", source: "web/rules.fix", destination: "/home/vagrant/rules.fix"
    web.vm.provision "shell", inline: <<-SHELL
      sudo chmod 644 /home/vagrant/rules.* 
      sudo chown root.root /home/vagrant/rules.*
      sudo mv -f /home/vagrant/rules.* /etc/iptables
    SHELL
    #Apply firewall rules and reboot
    web.vm.provision "shell", inline: "sudo iptables-restore /etc/iptables/rules.fix" #We need this to keep connection alive between vagrant and guest
    web.vm.provision "shell", inline: "sudo iptables-restore /etc/iptables/rules.v4", reboot: true
       
  end
 
end #End of the file *********************************************************************************************
