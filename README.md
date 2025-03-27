# SP25_DS5111_nrg6cb
Spring 2025 MSDS Class: Software and Automation Skills

[![Feature Validation](https://github.com/KazBarker/SP25_DS5111_nrg6cb/actions/workflows/validtions.yml/badge.svg)](https://github.com/KazBarker/SP25_DS5111_nrg6cb/actions/workflows/validtions.yml)

## Setup Sequence:
1. Run `sudo apt update`

2. [Generate an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and add it to your GitHub account:
	* Type `ssh-keygen -t ed25519 -C "your_email@example.com"`, using the email linked to your GitHub account - do not use a passkey when prompted

	* Copy the public half of the key by typing `cat id_yourkeyname.pub` (the default key name is `id_ed25519.pub`)

	* In your GitHub account (under Settings > SSH and GPG keys) add a new SSH key, pasting your copied key text into the **Key** field`

3. Navigate to your home directory and clone this repository

4. Install required packages and set global variables by navigating into the main folder of the cloned repo and typing: `. ./scripts/init.sh`

5. Finish setting up the environment by typing `make quick_start`. Fill out the fields for your global GitHub credentials when prompted
	* Type `source $(readlink activate)` to activate the environment
	* Type `deactivate` to deactivate the environment

> [!IMPORTANT]
> An `installations` folder will be added to your system outside the main repository folder, and will contain larger package files and data downloads. It can be removed easily by running `make cleanup`.

## Script Details
* `init.sh`: updates the environment and installs vital packages

* `setup_git_global_creds.sh`: takes user input and updates the .gitconfig file with GitHub credentials

* `install_chrome_headless.sh`
	* Updates the environment
	* Installs task-specific packages
	* Installs `https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb`
	* Checks chrome version and runs a sanity check using `https://example.com/` - after successful execution the raw html of [https://example.com/](https://example.com/) should be displayed.

* `requirements.txt`: a list of python packages to be installed (installation performed by the makefile when `make update` is run)

## Project Repo Structure
```
SP25_DS5111_nrg6cb/
├── LICENSE
├── README.md
├── activate -> ../installations/env/bin/activate
├── bin
│   ├── __init__.py
│   ├── __pycache__
│   │   └── ...
│   ├── gainers
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   └── ...
│   │   ├── base.py
│   │   ├── factory.py
│   │   ├── stockanalysis.py
│   │   ├── test.py
│   │   ├── wsj.py
│   │   └── yahoo.py
│   ├── normalize_csv.py
│   └── sample_adder.py
├── files
│   ├── crontab_contents.txt
│   └── messy_files
│       └── ...
├── get_gainer.py
├── makefile
├── projects
│   ├── gainers
│   │   ├── README.md
│   │   ├── analyses
│   │   ├── dbt_project.yml
│   │   ├── logs
│   │   │   └── dbt.log
│   │   ├── macros
│   │   ├── models
│   │   │   └── example
│   │   │       ├── my_first_dbt_model.sql
│   │   │       ├── my_second_dbt_model.sql
│   │   │       └── schema.yml
│   │   ├── seeds
│   │   ├── snapshots
│   │   ├── target
│   │   │   ├── compiled
│   │   │   │   └── gainers
│   │   │   │       └── models
│   │   │   │           └── example
│   │   │   │               ├── my_first_dbt_model.sql
│   │   │   │               └── my_second_dbt_model.sql
│   │   │   ├── graph.gpickle
│   │   │   ├── graph_summary.json
│   │   │   ├── manifest.json
│   │   │   ├── partial_parse.msgpack
│   │   │   ├── run
│   │   │   │   └── gainers
│   │   │   │       └── models
│   │   │   │           └── example
│   │   │   │               ├── my_first_dbt_model.sql
│   │   │   │               └── my_second_dbt_model.sql
│   │   │   ├── run_results.json
│   │   │   └── semantic_manifest.json
│   │   └── tests
│   └── logs
│       └── dbt.log
├── pylintrc
├── scripts
│   ├── init.sh
│   ├── install_chrome_headless.sh
│   ├── requirements.txt
│   └── setup_git_global_creds.sh
└── tests
    ├── __init__.py
    ├── __pycache__
    │   └── ...
    ├── gainer_loading_test.py
    ├── lab04_test.py
    └── system_test.py
```

> [!TIP]
> To update the tree structure above, navigate to the repo's parent directory and enter:
> 
> `tree SP25_DS5111_nrg6cb/ -I env`

## Downloading and Normalizing Gainers
* Gainers files can be downloaded and normalized by running `make gainers SRC=<type>`
    * `type` can be "yahoo", "wsj", "stockanalysis", or "test"
    * Normalized CSV files will be saved to the files directory

* To download and normalize all available gainer types at once, run `make all_gainers`

## Example Raw Data: wsjgainers
|ID|Name|Volume|Last|Chg|% Chg|
|:----------|:-|:------|:----|:---|:-----|
0|Quantum Biopharma Ltd. (QNTM)|78.6M|6.71|3.53|111.01
1|Cumberland Pharmaceuticals Inc. (CPIX)|18.5M|3.76|1.63|76.53
2|MiNK Therapeutics Inc. (INKT)|350.9K|12.03|4.17|53.05
3|Lixiang Education Holding Co. Ltd. ADR (LXEH)|917.2K|8.13|2.73|50.56
4|Yoshiharu Global Co. (YOSH)|337.4K|5.43|1.75|47.55
5|Evaxion Biotech A/S ADR (EVAX)|62.8M|3.27|0.87|36.25
6|Beyond Inc. (BYON)|9.7M|9.68|2.42|33.33
7|Flexsteel Industries Inc. (FLXS)|121.2K|63.05|14.85|30.81
8|Exagen Inc. (XGN)|1.1M|5.02|1.14|29.38
9|ModivCare Inc. (MODV)|2.1M|4.8|0.96|25.0
10|Nuvve Holding Corp. (NVVE)|15.1M|3.31|0.66|24.91
