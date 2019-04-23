#!/bin/bash
# Incremental Commit for Phishing Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

RunPartialCommit () {
# ****************************************
# Copy last tested files into root of repo
# ****************************************

cat ${TRAVIS_BUILD_DIR}/dev-tools/output/domains/ACTIVE/list | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt
cat ${TRAVIS_BUILD_DIR}/dev-tools/output/domains/INACTIVE/list | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt
cat ${TRAVIS_BUILD_DIR}/dev-tools/output/domains/INVALID/list | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt

# *********************************************************
# Modify Readme File
# *********************************************************

bash ${TRAVIS_BUILD_DIR}/dev-tools/modify-readme.sh

}

RunPartialCommit

# **********************
# Exit With Error Number
# **********************

exit ${?}
