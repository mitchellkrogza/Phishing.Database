#!/bin/bash
# Generator Script for Phishing.Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

# *******************************
# Input and Output File Variables
# *******************************

inputA=${TRAVIS_BUILD_DIR}/input-source/ALL-feeds.list
input1=${TRAVIS_BUILD_DIR}/input-source/openphish-feed.list
input2=${TRAVIS_BUILD_DIR}/input-source/illegalfawn-feed.list
input3=${TRAVIS_BUILD_DIR}/input-source/phishtank-feed.list
input4=${TRAVIS_BUILD_DIR}/input-source/mitchellkrog-feed.list
output=${TRAVIS_BUILD_DIR}/dev-tools/phishing-domains-ALL.list

# **************
# Temp Variables
# **************

outputtmp=${TRAVIS_BUILD_DIR}/phishing.tmp
feed1=${TRAVIS_BUILD_DIR}/input-source/openphish.list
feed2=${TRAVIS_BUILD_DIR}/input-source/phishtank.list
feed3=${TRAVIS_BUILD_DIR}/input-source/mitchellkrog.list
tmp=${TRAVIS_BUILD_DIR}/input-source/tmp.list

# *********************************************
# Get Travis CI Prepared for Committing to Repo
# *********************************************

PrepareTravis () {
    git remote rm origin
    git remote add origin https://${GH_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git
    git config --global user.email "${GIT_EMAIL}"
    git config --global user.name "${GIT_NAME}"
    git config --global push.default simple
    git checkout "${GIT_BRANCH}"
}

# **********************************************
# Fetch our feed(s) and append to our input file
# **********************************************

fetch () {
    sudo wget -q https://hosts.ubuntu101.co.za/openphish/openphish-feed.list -O ${feed1}
    cat ${feed1} >> ${input1}

    sudo wget -q https://hosts.ubuntu101.co.za/openphish/phishtank-feed.list -O ${feed2}
    cat ${feed2} >> ${input3}

    sudo wget -q https://hosts.ubuntu101.co.za/openphish/mitchellkrog-feed.list -O ${feed3}
    cat ${feed3} >> ${input4}

    sudo rm ${feed2}
    sudo rm ${feed1}
    sudo rm ${feed3}
}

# *************************************************
# Prepare our input lists and remove any duplicates
# *************************************************

initiate () {

    # Prepare Feed 1 / OpenPhish
    sort -u ${input1} -o ${input1}
    grep '[^[:blank:]]' < ${input1} > ${tmp}
    sudo mv ${tmp} ${input1}

    # Prepare Feed 2 / IllegalFawn
    sort -u ${input2} -o ${input2}
    grep '[^[:blank:]]' < ${input2} > ${tmp}
    sudo mv ${tmp} ${input2}

    # Prepare Feed 3 / Phishtank
    sort -u ${input3} -o ${input3}
    grep '[^[:blank:]]' < ${input3} > ${tmp}
    sudo mv ${tmp} ${input3}

    # Prepare Feed 4 / Mitchell Krog
    sort -u ${input4} -o ${input4}
    grep '[^[:blank:]]' < ${input4} > ${tmp}
    sudo mv ${tmp} ${input4}

}

# ***************************************
# Prepare our list for PyFunceble Testing
# ***************************************

prepare () {
    cat ${input1} > ${output}
    cat ${input2} >> ${output}
    cat ${input3} >> ${output}
    cat ${input4} >> ${output}
    cat ${output} > ${inputA}

    cut -d'/' -f3 ${output} > ${outputtmp}
    sort -u ${outputtmp} -o ${outputtmp}
    grep '[^[:blank:]]' < ${outputtmp} > ${output}
    sudo rm ${outputtmp}

    # Get dos2unix version
    dos2unix -V

    domain2idna -f ${output} -o ${output}
    dos2unix ${output}

    sort -u ${inputA} -o ${inputA}
    domain2idna -f ${inputA} -o ${inputA}
    dos2unix ${inputA}
}

# ****************************************
# Let's force update of dos2unix
# ****************************************
fixdos2unix () {

# Uninstall dos2unix first
sudo apt-get remove --purge dos2unix

# Download & Build dos2unix 7.4.0.1
cd /tmp
wget http://archive.ubuntu.com/ubuntu/pool/universe/d/dos2unix/dos2unix_7.4.0.orig.tar.gz
tar -xvf dos2unix_7.4.0.orig.tar.gz > /dev/null
cd dos2unix-7.4.0/
#./configure --prefix=/usr/local
PREFIX=/usr/bin
make -s
sudo make -s install
}

PrepareTravis
fetch
initiate
#fixdos2unix
prepare


# **********************
# Exit With Error Number
# **********************

exit ${?}
