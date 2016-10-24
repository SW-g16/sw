#!/usr/bin/env bash

mkdir -p $1
echo "Download path: "$1

echo
echo "Downloading votes..."
curl http://parltrack.euwiki.org/dumps/ep_votes.json.xz | xz -dc > $1/votes.json

echo
echo "Downloading MEPs..."
curl http://parltrack.euwiki.org/dumps/ep_meps_current.json.xz | xz -dc > $1/meps.json

echo
echo "Downloading Dossiers..."
curl http://parltrack.euwiki.org/dumps/ep_dossiers.json.xz | xz -dc > $1/dossiers.json
