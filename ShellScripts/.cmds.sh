source $SCRIPTS/.colours.sh
source $SCRIPTS/.help.sh

# GIT COMMANDS
alias gg='echo "\n\033[1;96mcloning repo from given address\033[0m\n" &! git clone'
alias gs='echo "\n\033[1;92mchecking branch status\033[0m\n" &! git status'
alias gu='echo "\n\033[1;92mpulling branch updates\033[0m\n" &! git pull'
alias gr='echo "\n\033[1;92mupdating remote repos \033[0m\n" &! git remote update'
alias ga='echo "\n\033[1;93madding all changes to commit queue \033[1;91m!!!\033[0m\n" &! git add * &! git add -u'
alias gc='echo "\n\033[1;93mcommiting change queue with given message\033[0m\n" &! git commit -m'
# alias gp='echo "\n\033[1;93mpushing commited changes to branch \033[1;91m!!!\033[0m\n" &! git push'
# alias gq='echo "\n\033[1;93mmaking quick commit \033[1;91m!!!\033[0m\n" &! $HOME/.gitquick.zsh'
# one for fetch
# one for merge from DEV
# one for merge from STABLE
# one for merge from MASTER
# use script to fix order issues (use gq script as example)

# ENV COMMANDS
alias BUILD="docker build -t project-transcendence ."
alias MAKE="docker run -it --name project-transcendence project-transcendence"
alias STOP="docker stop project-transcendence"
alias START="docker start -i project-transcendence"
alias DELETE="docker rm -f project-transcendence"
