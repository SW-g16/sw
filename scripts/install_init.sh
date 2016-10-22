#!/usr/bin/env bash

# Copy-paste these lines into a fresh install of Ubuntu 16.04 with Stardog 4.2 installed and running,
#   and the application should install successfully, so it can be run with init_session.sh

cd ~
sudo apt-get install git
git clone https://github.com/SW-g16/sw.git
sudo sh sw/install.sh
