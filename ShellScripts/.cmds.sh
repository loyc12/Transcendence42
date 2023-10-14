# source $SCRIPTS/.colours.sh
source $SCRIPTS/.help.sh

# GIT COMMANDS
alias GO='echo "\n > cloning repo from given address < \n" &! git clone' #									git optain
alias GS='echo "\n > checking branch status < \n" &! git status' #											git status
alias GP='echo "\n > pulling branch updates < \n" &! git pull' #											git pull
alias GU='echo "\n > updating remote repos  < \n" &! git remote update' #									git update (remote)
alias GA='echo "\n > adding all changes to commit queue \033[1;91m!!! < \n" &! git add * || git add -u' #	git add
alias GC='echo "\n > commiting change queue with given message < \n" &! git commit -m' #					git commit
alias GG='echo "\n > switching to given branch < \n" &! git switch' #										git go
alias GNB='echo "\n > ! creating new specified branch ! < \n" &! git push origin' #							git push-on-new-branch
alias GMRG='echo "\n > !! merging from given branch !! < \n" &! git merge' #								git merge
alias GPSH='echo "\n > !!! pushing commited changes to branch !!! < \n" &! git push' #						git push
alias GQCKP='echo "\n > !!!! making quick commit !!!! < \n" &! $SCRIPTS/.gitquick.sh' #						git quickpush


# one for fetch
# one for merge from DEV
# one for merge from STABLE
# one for merge from MASTER
# use script to fix order issues (use gq script as example)

# ENV COMMANDS
alias CONT_BUILD="docker build -t project-transcendence ."
alias CONT_MAKE="docker run -it --name project-transcendence project-transcendence"
alias CONT_STOP="docker stop project-transcendence"
alias CONT_START="docker start -i project-transcendence"
alias CONT_DELETE="docker rm -f project-transcendence"
