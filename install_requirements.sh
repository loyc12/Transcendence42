#!/bin/bash

#sudo apt-get -y update && sudo apt-get -y upgrade

#sudo apt-get -y install \
    #npm
    #...

#sudo npm install -g "@nestjs/cli"

#Install npm backend requirments (looks for package.json in the argument dir)
if [ -d "./backend" ] & [ -f "./backend/package.json" ]; then
    sudo npm install --prefix ./backend/transcendence_backend ./backend/transcendence_backend
fi

#Install npm frontend requirments
if [ -d "./frontend" ] && [ -f "./frontend/package.json" ]; then
    sudo npm install --prefix ./frontend/transcendence_frontend ./backend/transcendence_frontend
fi
    