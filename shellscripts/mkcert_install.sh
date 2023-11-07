BREW_DIR=$1
BREW_EXE=$2

echo $BREW_DIR
echo $BREW_EXE


#echo "curling homebrew installer"
/bin/bash -c "$(exec curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
#echo "curl homebrew installer DONE"
test -d ~/.linuxbrew && eval "$(~/.linuxbrew/bin/brew shellenv)"
#echo "test and shellenv DONE"
test -d $BREW_DIR && eval "$($BREW_EXE shellenv)"
#echo "test and shellenv DONE"
echo "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.bashrc
brew install mkcert