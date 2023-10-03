#!/bin/bash

echo "SET ENV FOR DOCKER COMMAND:"
echo "   BUILD (build image 1rst time)"
echo "   MAKE  (build container 1rst time)"
echo "   STOP  (stop container)"
echo "   START (start container)"
echo "   DELETE (destroy container)"

# -- SET ENV
export BUILD="docker build -t project-transcendence ."
export MAKE="docker run -it --name project-transcendence project-transcendence"
export STOP="docker stop project-transcendence"
export START="docker start -i project-transcendence"
export DELETE="docker rm -f project-transcendence"
export COMPOSE="docker-compose up"
export NEST_START="bash start_nest_srv_3000.sh"
export NGINX_START="bash ./sandbox/start_nginx_server.sh"
export NGINX_STOP="bash ./sandbox/stop_nginx_server.sh"