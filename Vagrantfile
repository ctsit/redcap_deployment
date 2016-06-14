# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  # Enable the vagrant env plugin
  config.env.enable

  config.vm.hostname = ENV["HOSTNAME_IN_GUEST"]
  config.vm.box = ENV["CONFIG_VM_BOX"]

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  config.vm.box_check_update = true

  config.vm.network "forwarded_port", guest: 80,  host: ENV["FORWARDED_PORT_80"]
  config.vm.network "forwarded_port", guest: 443, host: ENV["FORWARDED_PORT_443"]

  # Create a private network, which allows host-only access to the machine using a specific IP.
  config.vm.network "private_network", ip: ENV["VM_IP"]

  # Set the hostname using the vagrant hostupdater plugin
  config.hostsupdater.remove_on_suspend = false
  config.hostsupdater.aliases = [ENV["HOSTNAME_IN_HOST"]]

  config.vm.synced_folder "redcap", ENV["PATH_TO_APP_IN_GUEST_FILESYSTEM"],
    owner: "www-data",
    group: "vagrant"

  config.vm.provider "virtualbox" do |vb|
    # vb.memory = "1024"
    # Get virtual box name vagrant env plugin
    vb.name = ENV["HOSTNAME_IN_GUEST"]
  end

  # Run our customizations
  config.vm.provision "shell" do |s|
    s.path = "bootstrap.sh"
  end

  # Restart apache when all done (if using apache)
  config.vm.provision "shell", run: "always", inline: "service apache2 restart"

  # Help the developer to find the app :)
  if Vagrant.has_plugin?('vagrant-triggers')
    config.trigger.after [:up] do
      system("open -a 'Google Chrome.app' #{ENV['URL_OF_DEPLOYED_APP']}")
    end
  end

end
