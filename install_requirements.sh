#!/bin/bash

#sudo apt-get -y update && sudo apt-get -y upgrade

#sudo apt-get -y install \
    #npm
    #...

sudo yarn global add "@nestjs/cli"
sudo yarn global add "@angular/cli"
#sudo npm install -g "@angular/cli"

#Install npm backend requirments (looks for package.json in the argument dir)
if [ -d "./backend" ] & [ -f "./backend/package.json" ]; then
    cd backend
    yarn install --no-cache
    cd ..
    #sudo yarn install --prefix ./backend/transcendence_backend ./backend/transcendence_backend
fi

#Install npm frontend requirments
if [ -d "./frontend" ] && [ -f "./frontend/package.json" ]; then
    cd frontend
    yarn install --no-cache
    cd ..
    #sudo yarn install --prefix ./frontend/transcendence_frontend ./backend/transcendence_frontend
fi
    