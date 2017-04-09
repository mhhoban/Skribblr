# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|

  # configure skribblr-dev box
  config.vm.define "skribblr_dev" do |skribblr_dev|
    skribblr_dev.vm.box = "bento/ubuntu-16.04"
    skribblr_dev.vm.provision :shell, path: "vagrant_provision/skribblr_provision.sh"

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    # config.vm.network "forwarded_port", guest: 80, host: 8080
    skribblr_dev.vm.network :forwarded_port, guest: 8000, host: 8080

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"
  end
end
