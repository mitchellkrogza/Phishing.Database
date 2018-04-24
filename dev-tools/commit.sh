#!/bin/bash
# Commit Script for Phishing.Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

# ***********************************
# Copy tested files into root of repo
# ***********************************

cat ${TRAVIS_BUILD_DIR}/dev-tools/PyFunceble/output/domains/ACTIVE/list | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt
cat ${TRAVIS_BUILD_DIR}/dev-tools/PyFunceble/output/domains/INACTIVE/list | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt
cat ${TRAVIS_BUILD_DIR}/dev-tools/PyFunceble/output/domains/INVALID/list | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt

# *********************************************************
# Pull Fresh Data for our Next Tests and Modify Readme File
# *********************************************************

sudo chmod +x ${TRAVIS_BUILD_DIR}/dev-tools/pulldata.sh
sudo chmod +x ${TRAVIS_BUILD_DIR}/dev-tools/modify-readme.sh

sudo ${TRAVIS_BUILD_DIR}/dev-tools/pulldata.sh
sudo ${TRAVIS_BUILD_DIR}/dev-tools/modify-readme.sh

# *******************************
# Make sure Travis owns all files
# *******************************

sudo chown -R travis:travis ${TRAVIS_BUILD_DIR}/

# ***************
# Exit our Script
# ***************

exit ${?}


