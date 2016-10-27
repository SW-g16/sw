#!/usr/bin/env bash

source ask.sh

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $HERE
ls

if ask 'Download/Sync new govtrack data? (default: n)' N; then
  guake -n guake -e 'cd '$HERE' && echo && echo Hit ctrl-c at any point to stop the downloading! && sleep 2 && sh ../mine/govtrack/s/download.sh ../data/govtrack/' guake -r "GovTrack synch"
fi

if ask 'Download new parltrack data? (default: n)' N; then
  guake -n guake -e 'cd '$HERE' && echo && echo This retrieves parltrack archives, please let it finish, otherwise the data will be corrupt. && sleep 2 && sh ../mine/parltrack/s/download.sh ../data/parltrack/' guake -r "Parltrack Download"
fi

echo 'Please stop any data downloads before proceeding'

if ask 'Import new Govtrack vote data? (default: y)' Y; then
  #if ask 'Reset database first? (default: y)' Y; then
    #guake -n guake -e 'python '$1'/../scripts/reset-db.sh'
  #fi
  guake -n guake -e 'cd '$HERE' && python ../mine/govtrack \n '$STARDOG'/bin/stardog data add -g votes '$HERE'/../data/govtrack/govtrack.rdf' guake -r "Govtrack Semantifier"

fi

echo
echo 'Parltrack scripts do not currently handle importing, it will save a .trig file in the data dir.'
if ask 'Create new Parltrack vote data? (default: y)' Y; then
  guake -n guake -e 'cd '$HERE' && python ../mine/parltrack \n' $STARDOG'/bin/stardog data add -g votes '$HERE'/../data/parltrack/parltrack.trig' guake -r "Parltrack Semantifier"
fi

