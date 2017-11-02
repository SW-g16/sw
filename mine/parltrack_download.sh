#!/usr/bin/env bash

# todo call each command from within the parltrack method that uses it

if [ ! -f $1/votes.json ]; then
    curl http://parltrack.euwiki.org/dumps/ep_votes.json.xz | xz -dc > $1/votes.json
fi

if [ ! -f $1/meps.json ]; then
    curl http://parltrack.euwiki.org/dumps/ep_meps_current.json.xz | xz -dc > $1/meps.json
fi

if [ ! -f $1/dossiers.json ]; then
    curl http://parltrack.euwiki.org/dumps/ep_dossiers.json.xz | xz -dc > $1/dossiers.json
fi




