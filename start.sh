#!/bin/bash

# -- SET ENV
alias BUILD="docker build -t project-transcendence ."
alias MAKE="docker run -it --name project-transcendence project-transcendence"
alias STOP="docker stop project-transcendence"
alias START="docker start -i project-transcendence"
alias DELETE="docker rm -f project-transcendence"