# gq alias script

if [[ $(git status) -eq 0 ]]
then
	echo "\n\033[1;91mCannot use git here !!!\033[0m\n"
else
	if [[ $(git status | grep -c "MASTER") -gt 0 ]]
	then
		echo "\n\033[1;91mCannot use gitquick on branch MASTER !!!\033[0m\n"
	else
		if [[ $(git status | grep -c "STABLE") -gt 0 ]]
		then
			echo "\n\033[1;91mCannot use gitquick on branch STABLE !!!\033[0m\n"
		else
			git status || true
			git remote update || true
			git pull || true
			git status || true
			git add * || true
			git add -u || true
			git status || true
			git commit -m 'minor (gitquick)' || true
			git push || true
			echo "\n\033[1;92mDone !\033[0m\n"
		fi
	fi
fi

