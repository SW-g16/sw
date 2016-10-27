#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

git submodule init
git submodule update

sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update

sudo apt-get -y install default-jdk
sudo apt-get -y install default-jre
sudo apt-get -y install python-pip
sudo apt-get -y install python-software-properties python g++ make
sudo apt-get -y install nodejs
sudo apt-get -y install npm

sudo pip install flask
sudo pip install SPARQLWRAPPER

cd ~/sw/ld-r
./install
sudo bower install --allow-root
