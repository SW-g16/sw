#!/usr/bin/env bash

# this is for retrieving bulk data from govtrack.us , and must be run before the python importer
# run from the location where u want to store the data
# don't store data anywhere in sw - if your code editor indexes your files this will waste a lot of processing power

# TODO rewrite to --include only what we want instead of to --exclude all we don't want

mkdir -p $1
cd $1
echo "Download path: "$1

rsync -avz govtrack.us::govtrackdata/congress-legislators .
rsync -avz --delete-excluded --exclude='**amendments**' --exclude='**hjres**' --exclude='**sconres**' --exclude='**sjres**' --exclude='**.xml' --exclude='**hconres**' --exclude='**samdt**' --exclude='**hres**' --exclude='**sres**' --exclude='**/text-versions/' --exclude="**committee**" govtrack.us::govtrackdata/congress .
