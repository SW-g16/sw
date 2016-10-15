#!/usr/bin/env bash

# this script resets the database

cd ~/Software/stardog-4.1.3/bin
./stardog-admin db drop votes
./stardog-admin db create -n votes ~/sw/ontology.ttl