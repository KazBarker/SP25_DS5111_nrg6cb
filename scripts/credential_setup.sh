#!/usr/bin/bash

echo "Type github email then press ENTER:"
read USER

echo "Type github username then press ENTER:"
read NAME

echo "Type the name of the file containing your SSH key, then press ENTER (if default file, just press ENTER)"
read KEY

if ! test -d ~/.gitconfig; then
	mkdir ~/.gitconfig
	chmod 600 ~/.gitconfig
	echo "The folder .gitconfig has been added to your home directory."
fi

echo
CONF1=$(git config --global --list | tr '\n' '\n\011')
echo -e "Prior config:\n${CONF1}"

git config --global user.email ${USER}
git config --global user.name ${NAME}

CONF2=$(git config --global --list | tr '\n' '\n\011')
echo
echo -e "New config:\n${CONF2}"

echo
if [[ -z "$KEY" ]]; then
	ssh -T -i ~/.ssh/id_ed25519 git@github.com
else
	ssh -T -i ~/.ssh/${KEY} git@github.com
fi

