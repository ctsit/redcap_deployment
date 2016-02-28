# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "puppetlabs/debian-7.8-64-nocm"
  config.vm.hostname = "redcap-deployment"
  config.hostsupdater.remove_on_suspend = false
  config.hostsupdater.aliases = ["redcap.dev"]
  config.vm.network "private_network", ip: "192.168.33.113"
  config.vm.provision "shell" do |s|
    s.path = "bootstrap.sh"
  end
end

