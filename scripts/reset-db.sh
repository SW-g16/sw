#!/usr/bin/env bash

# this script resets the database

cd ~/Software/stardog-4.2/bin
./stardog-admin db drop votes
./stardog-admin db create -o reasoning.sameas=FULL search.enabled=TRUE -n votes ~/sw/ontology.ttl
