#!/bin/bash
# Commit Script for Phishing.Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

# ***********************************
# Copy tested files into root of repo
# ***********************************

statuses="ACTIVE INACTIVE INVALID"

for status in $(echo ${statuses})
do
    statusFile="${TRAVIS_BUILD_DIR}/dev-tools/output/domains/${status}/list"

    if [[ -f ${statusFile} ]]
    then
        cat ${statusFile} | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-domains-${status}-in-testing.txt
        cat ${statusFile} | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-domains-${status}.txt
    else
        echo "" > ${TRAVIS_BUILD_DIR}/phishing-domains-${status}-in-testing.txt
        echo "" > ${TRAVIS_BUILD_DIR}/phishing-domains-${status}.txt
    fi
done

# *********************************************************
# Modify Readme File
# *********************************************************

bash ${TRAVIS_BUILD_DIR}/dev-tools/modify-readme.sh

# ***************
# Exit our Script
# ***************

exit ${?}


