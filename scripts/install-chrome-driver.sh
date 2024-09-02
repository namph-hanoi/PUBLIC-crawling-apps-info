#!/bin/bash
set -eux
set -o pipefail

export BROWSER_MAJOR=114
wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$BROWSER_MAJOR -O chromedriver_version
wget https://chromedriver.storage.googleapis.com/`cat chromedriver_version`/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
