#!/usr/bin/env bash

# You're assumed to be on a fresh install of Ubuntu 16.04
#  and to have Stardog 4.2 installed.

cd ~

sudo apt-get install git
git clone https://github.com/SW-g16/sw.git
cd sw
git submodule init
git submodule update

cd scripts/old/install
sudo sh ./install-dependencies.sh
sudo sh ./install-ldr.sh
