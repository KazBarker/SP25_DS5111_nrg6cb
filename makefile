default:
	@cat makefile

help:
	@cat README.md

init:
	./scripts/init.sh

get_headless_browser:
	./scripts/install_chrome_headless.sh

setup_global_git_creds:
	./scripts/setup_git_global_creds.sh

env:
	python3 -m venv --system-site-packages ./installations/env; . ./installations/env/bin/activate; pip install --upgrade pip

update: env
	. ./installations/env/bin/activate; pip install -r ./scripts/requirements.txt

quick_start: init get_headless_browser setup_global_git_creds update

build_file_home:
	mkdir -p ./files

ygainers.html: build_file_home
	sudo google-chrome-stable --headless --disable-gpu --dump-dom --no-sandbox --timeout=5000 'https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=200' > ./files/ygainers.html

ygainers.csv: ygainers.html
	./installations/env/bin/python -c "import pandas as pd; raw = pd.read_html('./files/ygainers.html'); raw[0].to_csv('./files/ygainers.csv')"

wjsgainers.html: build_file_home
	sudo google-chrome-stable --headless --disable-gpu --dump-dom --no-sandbox --timeout=15000 https://www.wsj.com/market-data/stocks/us/movers > ./files/wjsgainers.html

wjsgainers.csv: wjsgainers.html
	./installations/env/bin/python -c "import pandas as pd; raw = pd.read_html('./files/wjsgainers.html'); raw[0].to_csv('./files/wjsgainers.csv')"

cleanup:
	sudo rm -rf ./installations
