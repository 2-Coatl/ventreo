# frozen_string_literal: true

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.hostname = "ventreo-ci"
  config.vm.synced_folder ".", "/workspace"

  config.vm.provider "virtualbox" do |vb|
    vb.cpus = 2
    vb.memory = 2048
  end

  config.vm.provision "shell", path: "scripts/provision_vagrant.sh"
end
