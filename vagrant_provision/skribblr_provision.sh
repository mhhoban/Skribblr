#!/bin/bash

sudo apt-get update

DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade 

sudo apt-get -y install python-pip python-dev libpq-dev postgresql postgresql-contrib

sudo apt-get -y install xvfb

sudo dpkg -i /vagrant/vagrant_provision/provision_resources/google-chrome-stable_current_amd64.deb

sudo apt-get -y install -f

sudo dpkg -i /vagrant/vagrant_provision/provision_resources/google-chrome-stable_current_amd64.deb

sudo pip install virtualenv

virtualenv /vagrant/venv/

sudo cp /vagrant/vagrant_provision/provision_resources/chromedriver /vagrant/venv/bin/
