#!/usr/bin/env bash

# run this upon changing ld-r code

cd ~/sw/
# insert our config code into ld-r
sudo cp -f -al ldr-config/* ld-r/configs/
