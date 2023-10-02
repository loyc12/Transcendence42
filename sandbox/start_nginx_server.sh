#!/bin/bash

BASE_PATH="/workspaces/Transcendence42"


echo "COPY NGINX CONFIG TO /etc/nginx/"
sudo cp ${BASE_PATH}/sandbox/nginx.conf /etc/nginx/

if [ -f /run/nginx.pid ]; then
    echo "RELOAD NGINX SERVER ..."
    sudo nginx -s reload
else 
    echo "INSTALLING NGINX ..."
    sudo apt-get install nginx
    echo "START NGINX ..."
    sudo nginx
fi

if [ -f /run/nginx.pid ]; then
    echo -n "TEST : CURL REQUEST TO localhost:8080 : "
    curl -X GET http://localhost:8080/
    echo
    echo "NGINX SERVER LISTENING ON PORT 8080 ..."
else
    echo -n "NGINX SERVER FAILED TO START !"
fi
