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

build_file_home:
	mkdir -p $(MY_DIR)/files

set_tz:
	sudo ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime

quick_start: init get_headless_browser setup_global_git_creds update set_tz

lint: build_file_home
	. $(INSTALLATION_DIR)/installations/env/bin/activate; find . -name "*.py" -printf '%p\n' -exec pylint {} \;

test: lint
	. $(INSTALLATION_DIR)/installations/env/bin/activate; pytest -vv tests

gainers: build_file_home
	. $(INSTALLATION_DIR)/installations/env/bin/activate; python get_gainer.py $(SRC)

all_gainers: build_file_home
	. $(INSTALLATION_DIR)/installations/env/bin/activate; python get_gainer.py wsj; python get_gainer.py yahoo; python get_gainer.py stockanalysis; python bin/prep_csv.py "files/"

export_gainers:
	. $(INSTALLATION_DIR)/installations/env/bin/activate; python bin/snowflake/flake_gainers.py "files/"; dbt run --project-dir projects/gainers_views

snowflake_views:
	. $(INSTALLATION_DIR)/installations/env/bin/activate; dbt run --project-dir projects/gainers_views

rebuild_snowflake:
	. $(INSTALLATION_DIR)/installations/env/bin/activate; python bin/snowflake/rebuild_snowflake.py; dbt run --project-dir projects/gainers_views

cleanup:
	sudo rm -rf $(INSTALLATION_DIR)/installations
