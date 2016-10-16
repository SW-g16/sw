#!/usr/bin/env bash

# run this upon changing ld-r code

cd ../
# insert our config code into ld-r
cp -f -al ldr-config/* ld-r/configs/
