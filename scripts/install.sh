#!/usr/bin/env bash

sudo apt-get install python-software-properties python g++ make
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs
sudo npm install webpack -g
sudo npm install bower -g
sudo npm install

cd ~/sw/

wget https://nodejs.org/dist/v6.7.0/node-v6.7.0-linux-x64.tar.xz
tar xf node-v6.7.0-linux-x64.tar.xz
rm node-v6.7.0-linux-x64.tar.xz

git clone https://github.com/ali1k/ld-r.git
cd ld-r

# this will throw a permission error, regardless of whether you're sudo. 
# this is ok. the error command (from the tutorial) is repeated with --allow-root below. 
sudo ./install

sudo bower install --allow-root

sudo find ~/sw/ld-r -type d -exec chmod 777 {} \;
sudo find ~/sw/node-v6.7.0-linux-x64 -type d -exec chmod 777 {} \;

sudo sh ~/sw/scripts/apply-config.sh

