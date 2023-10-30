# source $SCRIPTS/.colours.sh
source $SCRIPTS/.help.sh

# GIT COMMANDS
alias GO='echo "\n > cloning repo from given address < \n" &! git clone' #									git optain (clone)
alias GS='echo "\n > checking branch status < \n" &! git status' #											git status
alias GP='echo "\n > pulling branch updates < \n" &! git pull' #											git pull
alias GU='echo "\n > updating remote repos  < \n" &! git remote update' #									git update (remote upadte)
alias GA='echo "\n > adding all changes to commit queue \033[1;91m!!! < \n" &! git add * || git add -u' #	git add
alias GC='echo "\n > commiting change queue with given message < \n" &! git commit -m' #					git commit ...
alias GG='echo "\n > switching to given branch < \n" &! git switch' #										git go (switch)

alias GNB='echo "\n > ! creating new specified branch ! < \n" &! git push origin' #							git push (on new branch)
alias GMRG='echo "\n > !! merging from given branch !! < \n" &! git merge' #								git merge ...
alias GPSH='echo "\n > !!! pushing commited changes to branch !!! < \n" &! git push' #						git push
alias GQCKP='echo "\n > !!!! making quick commit !!!! < \n" &! $SCRIPTS/.gitquick.sh' #						git quickpush


# fetch origin && git reset --hard origin/<BRANCH>

# use script to fix order issues (use gq script as example)

# ENV COMMANDS
#alias CONT_BUILD="docker build -t project-transcendence ."
#alias CONT_MAKE="docker run -it --name project-transcendence project-transcendence"
#alias CONT_STOP="docker stop project-transcendence"
#alias CONT_START="docker start -i project-transcendence"

alias CONT_COMPOSE="docker compose up"
alias OS_UPDATE="sudo apt update | sudo apt upgrade"
