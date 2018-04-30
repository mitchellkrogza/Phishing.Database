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
totalexploits=$(wc -l < ${TRAVIS_BUILD_DIR}/input-source/ALL-feeds.list)
activesites=$(wc -l < ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt)
inactivesites=$(wc -l < ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt)
invalidsites=$(wc -l < ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt)
total=$((${activesites} + ${inactivesites} + ${invalidsites}))
percentactive=$(awk "BEGIN { pc=100*${activesites}/${total}; i=int(pc); print (pc-i<0.5)?i:i+1 }")
percentinactive=$(awk "BEGIN { pc=100*${inactivesites}/${total}; i=int(pc); print (pc-i<0.5)?i:i+1 }")
percentinvalid=$(awk "BEGIN { pc=100*${invalidsites}/${total}; i=int(pc); print (pc-i<0.5)?i:i+1 }")

# **************************************************
# Write Version and Exploit Count into the README.md
# **************************************************

updatereadme () {

printf '%s\n%s%s\n%s%s\n%s%s\n%s%s\n%s\n%s%s\n%s' "${startmarker}" "#### Version: " "${version}" "#### ACTIVE Unique Phishing Domains (Tested): " "[${activesites}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt) (${percentactive} %)" "#### INACTIVE Unique Phishing Domains (Tested): " "[${inactivesites}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-INACTIVE.txt) (${percentinactive} %)" "#### INVALID Unique Phishing Domains (Tested): " "[${invalidsites}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-INVALID.txt) (${percentinvalid} %)" "*****************************" "#### Total Phishing URL's: " "[${totalexploits}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/input-source/ALL-feeds.list) :exclamation: Large File" "${endmarker}" >> ${tmprdme}
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
