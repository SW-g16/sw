#!/usr/bin/env bash

cd ~/sw/ld-r

sudo npm install webpack
sudo npm install bower -g
sudo npm install

ln -s /usr/bin/nodejs /usr/bin/node

sudo ./install

sudo bower install --allow-root
