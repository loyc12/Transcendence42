# source $SCRIPTS/.colours.sh # does not work in codespace terminal
source $SCRIPTS/.help.sh

# GIT COMMANDS
alias GO='echo "\n > cloning repo from given address < \n" &! git clone' #									git optain (clone < repo-url >)
alias GS='echo "\n > checking branch status < \n" &! git status' #											git status
alias GP='echo "\n > pulling branch updates < \n" &! git pull' #											git pull
alias GU='echo "\n > updating remote repos  < \n" &! git remote update' #									git (remote) update
alias GA='echo "\n > adding all changes to commit queue \033[1;91m!!! < \n" &! git add * || git add -u' #	git add * & -u
alias GC='echo "\n > commiting change queue with given message < \n" &! git commit -m' #					git commit < message >
alias GL='echo "\n > listing all branches < \n" &! git branch -a' #											git list (branch -a)
alias GG='echo "\n > switching to given branch < \n" &! git switch' #										git go (switch)
alias GD='echo "\n > comparing given branches < \n" &! git diff' #											git diff < branch_1..branch_1 >

alias GNB='echo "\n > ! pushing to new branch ! < \n" &! git push origin' #									git new_branch (push origin < src_branch:new_branch >)
alias GDB='echo "\n > ! unfollowing given branch < \n" &! git branch -d' #									git delete_branch (branch -d)
alias GFT='echo "\n > ! fetching from given branch ! < \n" &! git fetch origin' #							git fetch origin/< branch >
alias GMRG='echo "\n > !! merging from given branch !! < \n" &! git merge' #								git merge < src_branch >
alias GPSH='echo "\n > !! pushing commited changes to branch !! < \n" &! git push' #						git push
alias GQCKP='echo "\n > !!! making quick commit !!! < \n" &! $SCRIPTS/.gitquick.sh' #						git quickpush
alias GRSET='echo "\n > !!! resetting branch to origin !!! < \n" &! git reset --hard origin/' #				git reset --hard origin/< branch >

#implement colours codes (for zsh terminals)
# use script to fix order issues (use gq script as example)
# implement a Y/n for dangerous commands

alias TEST='echo "\033[0;35m test \n"'

# ENV COMMANDS
#alias CONT_BUILD="docker build -t project-transcendence ."
#alias CONT_MAKE="docker run -it --name project-transcendence project-transcendence"
#alias CONT_STOP="docker stop project-transcendence"
#alias CONT_START="docker start -i project-transcendence"

#alias CONT_COMPOSE="docker compose up"
#alias OS_UPDATE="sudo apt update | sudo apt upgrade"
