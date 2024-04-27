#!/bin/bash
# Incremental Commit for Phishing Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

set -e

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

UpdateFiles () {
# ****************************************
# Copy last tested files into root of repo
# ****************************************

domainstatuses="ACTIVE INACTIVE INVALID"
linkstatuses="ACTIVE INACTIVE INVALID"
todaystatus="ACTIVE"

for status in $(echo ${domainstatuses})
do
    statusFile="${TRAVIS_BUILD_DIR}/phishing-domains/output/domains/${status}/list"

    if [[ -f ${statusFile} ]]
    then
        cat ${statusFile} | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-domains-${status}.txt
    else
        echo "" > ${TRAVIS_BUILD_DIR}/phishing-domains-${status}.txt
    fi
done

for linkstatus in $(echo ${linkstatuses})
do
    linkstatusFile="${TRAVIS_BUILD_DIR}/phishing-links/output/domains/${linkstatus}/list"

    if [[ -f ${linkstatusFile} ]]
    then
        cat ${linkstatusFile} | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-links-${linkstatus}.txt
    else
        echo "" > ${TRAVIS_BUILD_DIR}/phishing-links-${linkstatus}.txt
    fi
done

for statusnow in $(echo ${todaystatus})
do
    statusnowFile="${TRAVIS_BUILD_DIR}/phishing-links-last-hour/output/domains/${statusnow}/list"

    if [[ -f ${statusnowFile} ]]
    then
        cat ${statusnowFile} | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-links-${statusnow}-NOW.txt
    else
        echo "" > ${TRAVIS_BUILD_DIR}/phishing-links-${statusnow}-NOW.txt
    fi
done

for statustoday in $(echo ${todaystatus})
do
    statustodayFile="${TRAVIS_BUILD_DIR}/phishing-links-today/output/domains/${statustoday}/list"

    if [[ -f ${statustodayFile} ]]
    then
        cat ${statustodayFile} | grep -v "^$" | grep -v "^#" > ${TRAVIS_BUILD_DIR}/phishing-links-${statustoday}-TODAY.txt
    else
        echo "" > ${TRAVIS_BUILD_DIR}/phishing-links-${statustoday}-TODAY.txt
    fi
done

}

RunWhitelist () {
# *********************************************************
# Clean with whitelist
# *********************************************************

bash ${TRAVIS_BUILD_DIR}/dev-tools/whitelist.sh

# *********************************************************
# Modify Readme File
# *********************************************************

bash ${TRAVIS_BUILD_DIR}/dev-tools/modify-readme.sh
}


CommitData () {
commitdate=$(date +%F)
committime=$(date +%T)
timezone=$(date +%Z)
cd ${TRAVIS_BUILD_DIR}
git remote rm origin
git remote add origin https://${GH_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git
git config --global user.email "${GIT_EMAIL}"
git config --global user.name "${GIT_NAME}"
git config --global push.default simple
git checkout master
git add -A
git commit -am "V.${TRAVIS_BUILD_NUMBER} (${commitdate} ${committime} ${timezone}) [ci skip]"
git push origin master    
}

StripIPs () {
# STRIP FROM ACTIVE
grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt > ${TRAVIS_BUILD_DIR}/phishing-IPs-ACTIVE.txt
sort -u ${TRAVIS_BUILD_DIR}/phishing-IPs-ACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-IPs-ACTIVE.txt
sort -u ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt
grep -Fvxf ${TRAVIS_BUILD_DIR}/phishing-IPs-ACTIVE.txt ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt > ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVEtmp.txt
sudo mv ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVEtmp.txt ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt 
# STRIP FROM INACTIVE
grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt > ${TRAVIS_BUILD_DIR}/phishing-IPs-INACTIVE.txt
sort -u ${TRAVIS_BUILD_DIR}/phishing-IPs-INACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-IPs-INACTIVE.txt
sort -u ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt
grep -Fvxf ${TRAVIS_BUILD_DIR}/phishing-IPs-INACTIVE.txt ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt > ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVEtmp.txt
sudo mv ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVEtmp.txt ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt 
# STRIP FROM INVALID
grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt > ${TRAVIS_BUILD_DIR}/phishing-IPs-INVALID.txt
sort -u ${TRAVIS_BUILD_DIR}/phishing-IPs-INVALID.txt -o ${TRAVIS_BUILD_DIR}/phishing-IPs-INVALID.txt
sort -u ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt
grep -Fvxf ${TRAVIS_BUILD_DIR}/phishing-IPs-INVALID.txt ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt > ${TRAVIS_BUILD_DIR}/phishing-domains-INVALIDtmp.txt
sudo mv ${TRAVIS_BUILD_DIR}/phishing-domains-INVALIDtmp.txt ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt 
}


PrepareTravis
UpdateFiles
StripIPs
RunWhitelist
CommitData

# **********************
# Exit With Error Number
# **********************

exit ${?}
