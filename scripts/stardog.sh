#!/usr/bin/env bash


source ask.sh

echo "(Re)Initializing Stardog"

if [ -z "$STARDOG" ]; then

  # stardog env var is not set

  if ask "Search for the stardog directory? This may take a while. (default: n)" N; then
    echo 'Looking for stardog...'
    find $HOME -iname "*stardog-*" -type d 2> /dev/null
  fi

  answer=0

  while [ $answer == 0 ]

  do
    if (( $answer == 0 )); then
      read -p 'Please input the correct (full) path: ' STARDOG_PATH
    fi

    echo
    echo $STARDOG_PATH
    if ask "Is this the correct path? (default: y)" Y; then
        answer=1
    fi
  done

  # Add export to profile for persistence
  echo 'export STARDOG='$STARDOG_PATH >> ~/.profile
  source ~/.profile
fi

echo 'Stardog directory: '$STARDOG
cd $STARDOG/bin



# rm system.lock is the quickest way to restart stardog, and appears not to do any harm.
# an alternative to deleting this file is to send a shutdown signal to stardog,
# but this takes TIMEOUT seconds if stardog isn't already running

if ask 'Use sudo for stardog?'; then

  sudo rm -f ../system.lock
  sudo ./stardog-admin server start --disable-security

  # Create table
  if ask 'Reset votes table?'; then
    ABS_DIR=~/sw/scripts
    sudo ./stardog-admin db drop votes
    sudo ./stardog-admin db create -o reasoning.type=DL reasoning.sameas=FULL -n votes $ABS_DIR/../ontology.ttl
  fi
else
  rm -f ../system.lock
  ./stardog-admin server start --disable-security

  # Create table
  if ask 'Reset votes table?'; then
    ABS_DIR=~/sw/scripts
    ./stardog-admin db drop votes
    ./stardog-admin db create -o reasoning.type=DL reasoning.sameas=FULL -n votes $ABS_DIR/../ontology.ttl
  fi
fi
echo
