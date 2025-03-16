MY_DIR := $(abspath .)
INSTALLATION_DIR = $(abspath ..)

default:
	@cat makefile

help:
	@cat README.md

init:
	. $(MY_DIR)/scripts/init.sh; mkdir -p $(INSTALLATION_DIR)/installations; mkdir -p $(INSTALLATION_DIR)/installations/env

get_headless_browser:
	$(MY_DIR)/scripts/install_chrome_headless.sh $(INSTALLATION_DIR)

setup_global_git_creds:
	$(MY_DIR)/scripts/setup_git_global_creds.sh

env:
	python3 -m venv --system-site-packages $(INSTALLATION_DIR)/installations/env; . $(INSTALLATION_DIR)/installations/env/bin/activate; pip install --upgrade pip;

update: env
	. $(INSTALLATION_DIR)/installations/env/bin/activate; pip install -r $(MY_DIR)/scripts/requirements.txt

quick_start: init get_headless_browser setup_global_git_creds update

build_file_home:
	mkdir -p $(INSTALLATION_DIR)/files

lint:
	- find . -name "*.py" -printf '%p\n' -exec pylint {} \;

test: lint
	- pytest -vv tests

gainers:
	. $(INSTALLATION_DIR)/installations/env/bin/activate; python get_gainer.py $(SRC)
#	. ../installations/env/bin/activate; python get_gainer.py $(SRC)

cleanup:
	sudo rm -rf $(INSTALLATION_DIR)/installations; sudo rm -rf $(INSTALLATION_DIR)/files
