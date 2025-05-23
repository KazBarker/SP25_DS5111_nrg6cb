#!/bin/bash

MY_DIR=$1

sudo apt update
sudo apt install fonts-liberation -y
sudo wget --no-clobber -P "$MY_DIR/installations/chrome/" https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install "$MY_DIR/installations/chrome/google-chrome-stable_current_amd64.deb" -y
sudo apt --fix-broken install
sudo apt install "$MY_DIR/installations/chrome/google-chrome-stable_current_amd64.deb" -y

# Check Version of chrome and run a quick sanity check
google-chrome-stable --version
google-chrome-stable --headless --disable-gpu --dump-dom https://example.com/
