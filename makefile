MY_DIR := $(abspath .)
INSTALLATION_DIR = $(abspath ..)

default:
	@cat makefile

help:
	@cat README.md

init:
	$(MY_DIR)/scripts/init.sh; mkdir $(INSTALLATION_DIR)/installations; mkdir $(INSTALLATION_DIR)/installations/env

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

ygainers.html: build_file_home
	google-chrome-stable --headless --disable-gpu --dump-dom --no-sandbox --timeout=5000 'https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=200' > $(INSTALLATION_DIR)/files/ygainers.html

ygainers.csv: ygainers.html
	$(INSTALLATION_DIR)/installations/env/bin/python -c "import pandas as pd; raw = pd.read_html('$(INSTALLATION_DIR)/files/ygainers.html'); raw[0].to_csv('$(INSTALLATION_DIR)/files/ygainers.csv')"

wjsgainers.html: build_file_home
	google-chrome-stable --headless --disable-gpu --dump-dom --no-sandbox --timeout=15000 https://www.wsj.com/market-data/stocks/us/movers > $(INSTALLATION_DIR)/files/wjsgainers.html

wjsgainers.csv: wjsgainers.html
	$(INSTALLATION_DIR)/installations/env/bin/python -c "import pandas as pd; raw = pd.read_html('$(INSTALLATION_DIR)/files/wjsgainers.html'); raw[0].to_csv('$(INSTALLATION_DIR)/files/wjsgainers.csv')"

cleanup:
	sudo rm -rf $(INSTALLATION_DIR)/installations; sudo rm -rf $(INSTALLATION_DIR)/files
