#!/bin/bash
# Generator Script for Phishing.Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

# *******************************
# Input and Output File Variables
# *******************************

    # Phishing Feed Variables
    openphishFEED=${TRAVIS_BUILD_DIR}/input-source/openphish-feed.lst
    phishtankFEED=${TRAVIS_BUILD_DIR}/input-source/phishtank-feed.lst
    mitchellkrogFEED=${TRAVIS_BUILD_DIR}/input-source/mitchellkrog-feed.lst
    phishstatsFEED=${TRAVIS_BUILD_DIR}/input-source/phishstats-feed.lst
    illegalfawnFEED=${TRAVIS_BUILD_DIR}/input-source/illegalfawn-feed.lst

    # Phishing Feed Temp Files
    openphishTMP=${TRAVIS_BUILD_DIR}/input-source/openphish-tmp.lst
    phishtankTMP=${TRAVIS_BUILD_DIR}/input-source/phishtank-tmp.lst
    mitchellkrogTMP=${TRAVIS_BUILD_DIR}/input-source/mitchellkrog-tmp.lst
    phishstatsTMP=${TRAVIS_BUILD_DIR}/input-source/phishstats-tmp.lst

    # Full List Variables
    FullList=${TRAVIS_BUILD_DIR}/input-source/ALL-feeds.lst
    FullListURL=${TRAVIS_BUILD_DIR}/input-source/ALL-feeds-URLS.lst
    FullListURLsplit=${TRAVIS_BUILD_DIR}/input-source/ALL-feeds-URLS-part.
    FullListURLzip=${TRAVIS_BUILD_DIR}/input-source/ALL-feeds-URLS.tar.gz

    # PyFunceble Test List
    PyTestList=${TRAVIS_BUILD_DIR}/dev-tools/phishing-domains-ALL.lst

# **************
# Temp Variables
# **************

    tmp=${TRAVIS_BUILD_DIR}/input-source/tmp.list
    outputtmp=${TRAVIS_BUILD_DIR}/phishing.tmp
    urltmp=${TRAVIS_BUILD_DIR}/input-source/url.tmp

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

# ***************************
# Get Memory Usage for Travis
# ***************************

ShowSystemStats () {
    #egrep --color 'Mem|Cache|Swap' /proc/meminfo
    free -m
}

# **********************************************
# Fetch our feed(s) and append to our input file
# **********************************************

FetchData () {
    echo "*************"
    echo "Fetching Data"
    echo "*************"
    sudo wget -q https://hosts.ubuntu101.co.za/openphish/openphish-feed.list -O ${openphishFEED}

    sudo wget -q https://hosts.ubuntu101.co.za/openphish/phishtank-feed.list -O ${phishtankFEED}

    sudo wget -q https://hosts.ubuntu101.co.za/openphish/mitchellkrog-feed.list -O ${mitchellkrogFEED}

    sudo wget -q https://hosts.ubuntu101.co.za/openphish/phishstats-feed.list -O ${phishstatsFEED}
}

# ***************************************
# Prepare our list for PyFunceble Testing
# ***************************************

PrepareLists () {
    echo "**************"
    echo "Preparing Data"
    echo "**************"
    cat ${openphishFEED} >> ${FullList}
    cat ${phishtankFEED} >> ${FullList}
    cat ${mitchellkrogFEED} >> ${FullList}
    cat ${phishstatsFEED} >> ${FullList}
    #cat ${illegalfawnFEED} >> ${FullList}

    sudo truncate -s 0 ${FullListURL}
    cat ${openphishFEED} > ${FullListURL}
    cat ${phishtankFEED} >> ${FullListURL}
    cat ${mitchellkrogFEED} >> ${FullListURL}
    cat ${phishstatsFEED} >> ${FullListURL}
    #cat ${illegalfawnFEED} >> ${FullListURL}

    # Sort and Clean Domain List
    # **************************
    cut -d'/' -f3 ${FullList} > ${outputtmp}
    sort -u ${outputtmp} -o ${outputtmp}
    grep '[^[:blank:]]' < ${outputtmp} > ${FullList}

    # Sort and Clean the URL List
    # ***************************
    # Clean the URL List of Trailing and Ending Whitespace
    sort -u ${FullListURL} -o ${FullListURL}
    cat ${FullListURL} | sed 's/^[ \t]*//;s/[ \t]*$//' > ${urltmp}
    # Clean the URL List of trailing slashes and  final sort for duplicates
    cat ${urltmp} | sed 's:/*$::' > ${FullListURL}
    sort -u ${FullListURL} -o ${FullListURL}
    dos2unix ${FullListURL}

    # Remove Temporary Files
    # **********************
    sudo rm ${outputtmp}
    sudo rm ${urltmp}

    # Convert IDNA Domains and Make File Unix Friendly
    # ************************************************
    domain2idna -f ${FullList} -o ${FullList}
    dos2unix ${FullList}
    sudo cp ${FullList} ${PyTestList}

}

# Functions to split / zip files > May need this when we get close to the 100mb Github File Size Limit to Avoid using GIT LFS
# Here we split our URL file for bypassing the need for Git LFS
SplitFiles () {
    split -l 50000 --numeric-suffixes ${FullListURL} ${FullListURLsplit}
    #sudo rm ${FullListURL}
}
#SplitFiles

# Function to zip Files / Unused
ZipFiles () {
    tar -czvf ${FullListURLzip} ${FullListURL}
    #sudo rm ${FullListURL}
}
#ZipFiles

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
#FetchData
#PrepareLists
#ShowSystemStats
#fixdos2unix


# **********************
# Exit With Error Number
# **********************

exit ${?}
