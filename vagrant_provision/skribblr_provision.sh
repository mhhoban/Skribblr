#!/bin/bash

sudo apt-get update

sudo apt-get -y upgrade

sudo apt-get -y install python-pip python-dev libpq-dev postgresql postgresql-contrib

sudo pip install virtualenv

virtualenv /vagrant/venv

