#!/bin/bash
# Generator Script for Phishing.Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

input=${TRAVIS_BUILD_DIR}/input-source/exploits.list
output=${TRAVIS_BUILD_DIR}/phishing.list
outputtmp=${TRAVIS_BUILD_DIR}/phishing.tmp
feed1=${TRAVIS_BUILD_DIR}/input-source/openphish.list
tmp=${TRAVIS_BUILD_DIR}/input-source/tmp.list

# *******************************************
# Fetch our feed and append to our input file
# *******************************************

fetch () {
sudo wget https://openphish.com/feed.txt -O ${TRAVIS_BUILD_DIR}/input-source/openphish.list
cat ${feed1} >> ${input}
sudo rm ${feed1}
}

# ************************************************
# Prepare our input list and remove any duplicates
# ************************************************

initiate () {
sort -u ${input} -o ${input}
grep '[^[:blank:]]' < ${input} > ${tmp}
sudo mv ${tmp} ${input}
}

# ***************************************
# Prepare our list for PyFunceble Testing
# ***************************************

prepare () {
sudo truncate -s 0 ${output}
sudo cp ${input} ${output}
cut -d'/' -f3 ${output} > ${outputtmp}
sort -u ${outputtmp} -o ${outputtmp}
grep '[^[:blank:]]' < ${outputtmp} > ${output}
sudo rm ${outputtmp}
dos2unix ${output}
}


fetch
initiate
prepare

# **********************
# Exit With Error Number
# **********************

exit ${?}


