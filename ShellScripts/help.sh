#!/bin/bash

echo "SET ENV FOR DOCKER COMMAND:"
echo "   BUILD (build image 1rst time)"
echo "   MAKE  (build container 1rst time)"
echo "   STOP  (stop container)"
echo "   START (start container)"
echo "   DELETE (destroy container)"

# -- SET ENV
alias BUILD="docker build -t project-transcendence ."
alias MAKE="docker run -it --name project-transcendence project-transcendence"
alias STOP="docker stop project-transcendence"
alias START="docker start -i project-transcendence"
alias DELETE="docker rm -f project-transcendence"