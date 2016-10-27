#!/bin/bash

source ~/.profile

SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $SCRIPTS_DIR

source ask.sh

bash stardog.sh

cd $SCRIPTS_DIR

bash ldr.sh $SCRIPTS_DIR

cd $SCRIPTS_DIR

bash mine.sh

echo
echo 'All programs/scrics/modules inited. Tailing stardog log. ' # best term?

tail -f $STARDOG/stardog.log
