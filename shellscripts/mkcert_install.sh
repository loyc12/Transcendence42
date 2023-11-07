#!/bin/sh
#BREW_DIR=$1
#BREW_EXE=$2
MKCERT_PATH=$1

#echo $BREW_DIR
#echo $BREW_EXE
echo "MKCERT PATH : " $MKCERT_PATH


wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64
sudo mv "mkcert-v1.4.3-linux-amd64" $MKCERT_PATH
sudo chmod +x $MKCERT_PATH
mkcert --version


#echo "curling homebrew installer"
#/bin/bash -c "$(exec curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
#echo "curl homebrew installer DONE"
#test -d ~/.linuxbrew && eval "$(~/.linuxbrew/bin/brew shellenv)"
#echo "test and shellenv DONE"
#test -d $BREW_DIR && eval "$($BREW_EXE shellenv)"
#echo "test and shellenv DONE"
#echo "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.bashrc
#brew install mkcert