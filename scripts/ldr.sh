#!/usr/bin/env bash


source ask.sh

# start ld-r
if ask 'start LD-R in dev (else build) mode? (default: n)' N; then
  guake -n guake -e 'cd '$1'/../ld-r && npm run dev' guake -r 'LD-R Dev'
else
  guake -n guake -e 'cd '$A1'/../ld-r && npm run build' guake -r 'LD-R Build'
fi

echo 'LD-R started in new terminal window'
echo
