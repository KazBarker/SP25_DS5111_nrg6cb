# SP25_DS5111_nrg6cb
Spring 2025 MSDS Class: Software and Automation Skills

## Setup Sequence:
1. Run `sudo apt update`

2. [Generate an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and add it to your GitHub account:
	* Type `ssh-keygen -t ed25519 -C "your_email@example.com"`, using the email linked to your GitHub account - do not use a passkey when prompted

	* Copy the public half of the key by typing `cat id_yourkeyname.pub` (the default key name is `id_ed25519.pub`)

	* In your GitHub account (under Settings > SSH and GPG keys) add a new SSH key, pasting your copied key text into the **Key** field`

3.  Navigate to your home directory and clone this repository

4.  Navigate into the main folder of the cloned repository and install some basic packages by typing `./scripts/init.sh`

5. Finish setting up the environment by typing `make quick_start`. Fill out the fields for your global GitHub credentials when prompted.

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
├── examples
│   ├── example_wjsgainers.csv
│   └── example_ygainers.csv
├── makefile
└── scripts
    ├── init.sh
    ├── install_chrome_headless.sh
    ├── requirements.txt
    └── setup_git_global_creds.sh

3 directories, 9 files
```

## Example Output: wjsgainers
Example CSV files can be found in the `examples` directory.

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
11|Palantir Technologies Inc. (PLTR)|230.8M|103.83|20.09|23.99
12|Vislink Technologies Inc. (VISL)|333.6K|2.51|0.48|23.65
13|3D Systems Corp. (DDD)|8.7M|4.62|0.88|23.53
14|One Stop Systems Inc. (OSS)|661.4K|4.3|0.78|22.16
15|Tuya Inc. ADR (TUYA)|5.2M|2.98|0.5|20.16
16|Jinxin Technology Holding Co. ADR (NAMI)|53.1K|2.87|0.46|19.0
17|Creative Medical Technology Holdings Inc. (CELZ)|101.4K|3.76|0.59|18.61
18|Absci Corp. (ABSI)|12.4M|4.35|0.65|17.57
