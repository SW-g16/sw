#!/usr/bin/env bash

# this script starts stardog, or forces a restart if it's already running

cd ~/Software/stardog-4.2
rm system.lock -f
cd bin
sudo ./stardog-admin server start --disable-security
