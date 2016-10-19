#!/usr/bin/env bash

sudo apt-get install git
git clone https://github.com/Ysgorg/sw.git
cd sw
git submodule init
git submodule update
