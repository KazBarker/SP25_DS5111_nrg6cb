#!/usr/bin/bash

echo -e "\n--------------------------------------------------------------------------------"
echo -e "--------------------------------------------------------------------------------"
echo -e "Type github email then press ENTER:"
read USER

echo -e "\nType github username then press ENTER:"
read NAME

echo -e "\nType the name of the file containing your SSH key, then press ENTER (if default file, just press ENTER)"
read KEY

if [ ! -f ~/.gitconfig ]; then
	touch ~/.gitconfig
	chmod 600 ~/.gitconfig
	echo -e "\nA .gitconfig file has been added to your home directory."
fi

CONF1=$(git config --global --list | tr '\n' '\n\011')
echo -e "\nPrior config:\n${CONF1}"

git config --global user.email ${USER}
git config --global user.name ${NAME}

CONF2=$(git config --global --list | tr '\n' '\n\011')
echo -e "\nNew config:\n${CONF2}"

echo
if [[ -z "$KEY" ]]; then
	ssh -T -i ~/.ssh/id_ed25519 git@github.com || true
else
	ssh -T -i ~/.ssh/${KEY} git@github.com || true
fi
echo -e "--------------------------------------------------------------------------------"
echo -e "--------------------------------------------------------------------------------\n"
