#!/usr/bin/env bash
sudo sh ~/sw/scripts/init_session.sh & 
~/Software/idea-IU-162.1628.40/bin/idea.sh & 
cd ~/sw/ldr_/ld-r/ 
npm run dev &

echo "\n\n\n\n Started errything"
