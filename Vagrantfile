# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"

  # Buildbot port
  config.vm.network :forwarded_port, guest: 8010, host: 8888
  config.vm.network :forwarded_port, guest: 9989, host: 9989
  config.vm.network :forwarded_port, guest: 8310, host: 8310

  ## For masterless, mount your salt file root
  config.vm.synced_folder "salt/", "/srv/"

  ## Use all the defaults:
  config.vm.provision :salt do |salt|
    salt.minion_config = "salt/minion"
    salt.run_highstate = true
    salt.verbose = true
  end
end
