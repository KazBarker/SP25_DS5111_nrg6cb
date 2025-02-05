# SP25_DS5111_nrg6cb
Spring 2025 MSDS Class: Software and Automation Skills

## Setup Sequence:
1. Run `sudo apt update`

2. [Generate an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and add it to your GitHub account:
	* Type `ssh-keygen -t ed25519 -C "your_email@example.com"`, using the email linked to your GitHub account - do not use a passkey when prompted

	* Copy the public half of the key by typing `cat id_yourkeyname.pub` (the default key name is `id_ed25519.pub`)

	* In your GitHub account (under Settings > SSH and GPG keys) add a new SSH key, pasting your copied key text into the **Key** field

3.  Navigate to your home directory and clone this repository

4.  Navigate into the main folder of the cloned repository and install some basic packages by typing `./scripts/init.sh`

5. Finish setting up the environment by typing `make quick_start`. Fill out the fields for your global GitHub credentials when prompted.

## Example Output: ygainers
|Unnamed: 2|Symbol|Name|Price|Change|Change %|Volume|Avg Vol (3M)|Market Cap|P/E Ratio (TTM)|52 Wk Change %|52 Wk Range|
|:------|:----|:----------|:-----|:------|:--------|:------|:------------|:----------|:---------------|:--------------|:-----------|
0|PLTR|Palantir Technologies Inc.||103.83 +20.09 (+23.99%)|20.09|+23.99%|228.64M|82.568M|236.527B|432.63|254.83%|
1|SPOT|Spotify Technology S.A.||621.77 +72.69 (+13.24%)|72.69|+13.24%|6.513M|2.695M|125.647B|177.14|127.99%|
2|GRAB|Grab Holdings Limited||5.11 +0.57 (+12.56%)|0.57|+12.56%|75.962M|34.733M|20.578B|-|37.58%|
3|IFNNY|Infineon Technologies AG||35.70 +3.72 (+11.63%)|3.72|+11.63%|86616|271133|48.406B|25.68|-7.29%|
4|SOUN|"SoundHound AI, Inc."||15.71 +1.47 (+10.32%)|1.47|+10.32%|52.354M|75.853M|6.179B|-|732.75%|
5|MP|MP Materials Corp.||24.47 +2.24 (+10.08%)|2.24|+10.08%|8.822M|2.97M|3.994B|-|34.32%|
6|ATI|ATI Inc.||63.72 +5.76 (+9.94%)|5.76|+9.94%|4.646M|1.392M|9.089B|24.51|44.39%|
7|FQVLF|First Quantum Minerals Ltd.||13.29 +1.17 (+9.65%)|1.17|+9.65%|17993|228076|11.087B|-|35.08%|
8|PBF|PBF Energy Inc.||30.35 +2.63 (+9.49%)|2.63|+9.49%|2.735M|2.094M|3.494B|-|-47.24%|
9|CLS|Celestica Inc.||131.98 +11.10 (+9.18%)|11.1|+9.18%|5.343M|3.148M|15.401B|36.56|232.45%|
10|DASTY|Dassault Systèmes SE||42.00 +3.52 (+9.15%)|3.52|+9.15%|21021|174567|56.238B|47.73|-17.81%|
11|SMCI|"Super Micro Computer, Inc."||29.16 +2.31 (+8.60%)|2.31|+8.60%|35.362M|69.744M|17.075B|13.38|-60.72%|
12|LANC|Lancaster Colony Corporation||180.96 +14.46 (+8.68%)|14.46|+8.68%|389508|133186|4.989B|28.72|-11.27%|
13|PDD|PDD Holdings Inc.||114.05 +8.81 (+8.37%)|8.81|+8.37%|12.991M|9.68M|158.389B|10.27|-18.28%|
14|XPEV|XPeng Inc.||16.99 +1.30 (+8.29%)|1.3|+8.29%|15.477M|11.593M|15.986B|-|86.12%|
15|AXTA|Axalta Coating Systems Ltd.||38.01 +2.90 (+8.26%)|2.9|+8.26%|4.803M|1.721M|8.289B|23.76|7.86%|
16|GBOOF|"Grupo Financiero Banorte, S.A.B. de C.V."||7.23 +0.55 (+8.23%)|0.55|+8.23%|198800|23738|20.339B|7.45|-32.96%|
17|AI|"C3.ai, Inc."||33.77 +2.56 (+8.20%)|2.56|+8.20%|5.133M|7.847M|4.359B|-|20.83%|
18|CLF|Cleveland-Cliffs Inc.||10.52 +0.78 (+8.01%)|0.78|+8.01%|13.61M|14.745M|5.196B|-|-50.76%|

## Example Output: wjsgainers
|Unnamed: 0|Volume|Last|Chg|% Chg|
|:----------|:------|:----|:---|:-----|
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
