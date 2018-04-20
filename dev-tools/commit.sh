#!/bin/bash
# Commit Script for Fail2Ban.WebExploits
# REPO: https://github.com/mitchellkrogza/Fail2Ban.WebExploits
# Copyright Mitchell Krog - mitchellkrog@gmail.com

tmprdme=tmprdme
tmprdme2=tmprdme2
version=V0.1.${TRAVIS_BUILD_NUMBER}
versiondate="$(date)"
startmarker="_______________"
endmarker="____________________"
totalexploits=$(wc -l < ${TRAVIS_BUILD_DIR}/phishing.list)

# **************************************************
# Write Version and Exploit Count into the README.md
# **************************************************

updatereadme () {

printf '%s\n%s%s\n%s%s\n%s' "${startmarker}" "#### Version: " "${version}" "#### Total Phishing Domains: " "${totalexploits}" "${endmarker}" >> ${tmprdme}
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


