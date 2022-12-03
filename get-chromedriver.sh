#!/bin/bash -e

BASE_URL='https://chromedriver.storage.googleapis.com'
LATEST_RELEASE=`wget -qO - ${BASE_URL}/LATEST_RELEASE`

# download driver.
wget ${BASE_URL}/${LATEST_RELEASE}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d src/
rm chromedriver_linux64.zip

# list of available drivers:
# echo "${BASE_URL}/index.html?path=${LATEST_RELEASE}/"
#   - chromedriver_mac64.zip
#   - chromedriver_mac_arm64.zip
#   - chromedriver_win32.zip
