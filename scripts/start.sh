#!/bin/bash

function ask() {
    # http://djm.me/ask
    local prompt default REPLY

    while true; do

        if [ "${2:-}" = "Y" ]; then
            prompt="Y/n"
            default=Y
        elif [ "${2:-}" = "N" ]; then
            prompt="y/N"
            default=N
        else
            prompt="y/n"
            default=
        fi

        # Ask the question (not using "read -p" as it uses stderr not stdout)
        echo -n "$1 [$prompt] "

        # Read the answer (use /dev/tty in case stdin is redirected from somewhere else)
        read REPLY </dev/tty

        # Default?
        if [ -z "$REPLY" ]; then
            REPLY=$default
        fi

        # Check if the reply is valid
        case "$REPLY" in
            Y*|y*) return 0 ;;
            N*|n*) return 1 ;;
        esac

    done
}

source ~/.profile
ABS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $ABS_DIR

# If stardog env var is not set...
if [ -z "$STARDOG" ]; then
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
echo
./stardog-admin server start --disable-security
echo

# Create table
if ask 'Reset votes table?'; then
  ./stardog-admin db drop votes
  ./stardog-admin db create -n votes $ABS_DIR/../ontology.ttl
fi
echo

cd $ABS_DIR

# Old framework
cd ../code
x-terminal-emulator -e "python src/main.py &"
echo 'Old framework started in new terminal window'
echo

# start ld-r
cd ../ld-r
if ask 'start LD-R in dev mode? (default: n)' N; then
  x-terminal-emulator -e "npm run dev &"
else
  x-terminal-emulator -e "npm run build &"
fi

echo 'LD-R started in new terminal window'
echo

if ask 'Import new vote data? (default: y)' Y; then
  python ../importer/importer.py
fi

echo
echo 'Done!'
