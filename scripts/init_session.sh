#!/usr/bin/env bash

guake -n guake -e 'cd ~/sw/scripts/ && sh ./stardog.sh' guake -r 'Stardog'

guake -n guake -e 'sh ~/sw/scripts/db_puter.sh' guake -r 'App'

guake -n guake -e 'cd ~/sw/ld-r && npm run dev &' guake -r 'LD-R'
