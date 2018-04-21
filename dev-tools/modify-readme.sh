#!/bin/bash
# Modify README.md Script for Phishing.Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

tmprdme=tmprdme
tmprdme2=tmprdme2
version=V0.1.${TRAVIS_BUILD_NUMBER}
versiondate="$(date)"
startmarker="_______________"
endmarker="____________________"
totalexploits=$(wc -l < ${TRAVIS_BUILD_DIR}/phishing.list)
activesites=$(wc -l < ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt)
inactivesites=$(wc -l < ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt)


# **************************************************
# Write Version and Exploit Count into the README.md
# **************************************************

updatereadme () {

printf '%s\n%s%s\n%s%s\n%s%s\n%s\n%s%s\n%s' "${startmarker}" "#### Version: " "${version}" "#### Active Phishing Domains (Tested): " "${activesites}" "#### Inactive Phishing Domains (Tested): " "${inactivesites}" "*****************************" "#### Domains to be tested on next run: " "${totalexploits}" "${endmarker}" >> ${tmprdme}
mv ${tmprdme} ${tmprdme2}
ed -s ${tmprdme2}<<\IN
1,/_______________/d
/____________________/,$d
,d
.r /home/travis/build/mitchellkrogza/Phishing.Database/README.md
/_______________/x
.t.
.,/____________________/-d
w /home/travis/build/mitchellkrogza/Phishing.Database/README.md
q
IN
rm ${tmprdme2}
}

updatereadme

exit ${?}

