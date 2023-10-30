# source $SCRIPTS/.colours.sh

alias HELP="$SCRIPTS/.help.sh"

echo ""
echo " >>> HELP MENU <<< "
echo ""
echo "GIT SHORTCUTS :"
echo ""
echo "    GO   : git optain < repo-url >       : git clone ..."
echo "    GS   : git status                    : git status"
echo "    GP   : git pull                      : git pull"
echo "    GU   : git update                    : git remote update"
echo "    GA   : git add                       : git add * & -u"
echo "    GC   : git commit < message >        : git commit ..."
echo "    GL   : git list                      : git list"
echo "    GG   : git go < dst-branch-name >    : git switch ..."
echo ""
echo "    GNB  : git new branch                : git push origin < branch1:branch2 >"
echo "    GDB  : git delete branch             : git branch -d <branch>"
echo "    GMRG : git merge < src-branch-name > : git merge ..."
echo "    GPSH : git push                      : git push"
echo "    GCQP : git quickpush                 : ( add, commit and push with comment \"minor\" )"
echo ""

alias GL='echo "\n > listing all branches < \n" &! git branch -a' #					git list (branch -a)
alias GDB='echo "\n > ! unfollowing given branch < \n" &! git branch -d' #		git delete branch (branch -d)


# echo ""
# echo "DOCKER ENV COMMANDS :"
# echo "   CONT_BUILD  : build image             : 1st time only"
# echo "   CONT_MAKE   : build container         : 1st time only"
# echo "   CONT_START  : start container"
# echo "   CONT_STOP   : stop container"
# echo "   CONT_DELETE : destroy container"
# echo ""
# echo "   CONT_CONST  : run docker composer"
# echo "   OS_UPDATE   : update et upgrade"