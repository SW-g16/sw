cd ~/sw/

sudo rm -r -f ldr_

mkdir ldr_
cd ldr_

wget https://nodejs.org/dist/v6.7.0/node-v6.7.0-linux-x64.tar.xz
echo "\n\n###untar\n\n\n"
tar xf node-v6.7.0-linux-x64.tar.xz
echo "\n\n###install webpack\n\n\n"
sudo npm install webpack -g

echo "\n\n###install bower\n\n\n"
sudo npm install bower -g
echo "\n\n###git clone\n\n\n"
git clone https://github.com/ali1k/ld-r.git
cd ld-r

echo "\n\n### install\n\n\n"
# this will throw a permission error, regardless of whether you're sudo. 
# this is ok. the error command (from the tutorial) is repeated with --allow-root below. 
sudo ./install
sudo bower install --allow-root

# you can now run 'sudo npm run dev' from the ldr_/ld-r directory
# the localhost address it hosts should be output to the terminal
# visit it. 
# if it loads with bootstrap and all, everything worked. 

