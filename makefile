MY_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

default:
	@cat makefile

help:
	@cat README.md

init:
	$(MY_DIR)/scripts/init.sh

get_headless_browser:
	$(MY_DIR)/scripts/install_chrome_headless.sh

setup_global_git_creds:
	$(MY_DIR)/scripts/setup_git_global_creds.sh

env:
	python3 -m venv --system-site-packages $(MY_DIR)/installations/env; . $(MY_DIR)/installations/env/bin/activate; pip install --upgrade pip

update: env
	. $(MY_DIR)/installations/env/bin/activate; pip install -r $(MY_DIR)/scripts/requirements.txt

quick_start: init get_headless_browser setup_global_git_creds update

build_file_home:
	mkdir -p $(MY_DIR)/files

ygainers.html: build_file_home
	sudo google-chrome-stable --headless --disable-gpu --dump-dom --no-sandbox --timeout=5000 'https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=200' > $(MY_DIR)/files/ygainers.html

ygainers.csv: ygainers.html
	$(MY_DIR)/installations/env/bin/python -c "import pandas as pd; raw = pd.read_html('$(MY_DIR)/files/ygainers.html'); raw[0].to_csv('$(MY_DIR)/files/ygainers.csv')"

wjsgainers.html: build_file_home
	sudo google-chrome-stable --headless --disable-gpu --dump-dom --no-sandbox --timeout=15000 https://www.wsj.com/market-data/stocks/us/movers > $(MY_DIR)/files/wjsgainers.html

wjsgainers.csv: wjsgainers.html
	$(MY_DIR)/installations/env/bin/python -c "import pandas as pd; raw = pd.read_html('$(MY_DIR)/files/wjsgainers.html'); raw[0].to_csv('$(MY_DIR)/files/wjsgainers.csv')"

cleanup:
	sudo rm -rf $(MY_DIR)/installations; sudo rm -rf $(MY_DIR)/files
