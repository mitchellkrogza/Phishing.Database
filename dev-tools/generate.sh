#!/bin/bash
# Generator Script for Fail2Ban.WebExploits
# REPO: https://github.com/mitchellkrogza/Fail2Ban.WebExploits
# Copyright Mitchell Krog - mitchellkrog@gmail.com

tmprdme=tmprdme
tmprdme2=tmprdme2
input=${TRAVIS_BUILD_DIR}/input-source/exploits.list
output=${TRAVIS_BUILD_DIR}/phishing.list
outputtmp=${TRAVIS_BUILD_DIR}/phishing.tmp
feed1=${TRAVIS_BUILD_DIR}/input-source/openphish.list
tmp=${TRAVIS_BUILD_DIR}/input-source/tmp.list
version=V0.1.${TRAVIS_BUILD_NUMBER}
versiondate="$(date)"
startmarker="_______________"
endmarker="____________________"
totalexploits=$(wc -l < ${TRAVIS_BUILD_DIR}/phishing.list)

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

# ******************************
# Now add and commit the changes
# ******************************

commit () {
cd ${TRAVIS_BUILD_DIR}

# *******************************
# Remove Remote Added by TravisCI
# *******************************

git remote rm origin

# **************************
# Add Remote with Secure Key
# **************************

git remote add origin https://${GH_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git

# *********************
# Set Our Git Variables
# *********************

git config --global user.email "${GIT_EMAIL}"
git config --global user.name "${GIT_NAME}"
git config --global push.default simple

# *******************************************
# Make sure we have checked out master branch
# *******************************************

git checkout master

# *******************************************************
# Add all the modified files, commit and push the changes
# *******************************************************

git add -A
git commit -am "V0.1.${TRAVIS_BUILD_NUMBER} [ci skip]"
sudo git push origin master
}

# **********************
# Run PyFunceble Testing
# **********************
# ****************************************************************
# This uses the awesome PyFunceble script created by Nissar Chababy
# Find PyFunceble at: https://github.com/funilrys/PyFunceble
# ****************************************************************

PyFunceble () {

yeartag=$(date +%Y)
monthtag=$(date +%m)
sudo chown -R travis:travis ${TRAVIS_BUILD_DIR}/
sudo chmod +x ${TRAVIS_BUILD_DIR}/dev-tools/PyFunceble/PyFunceble.py
cd ${TRAVIS_BUILD_DIR}/dev-tools/PyFunceble/
export TRAVIS_BUILD_DIR=${TRAVIS_BUILD_DIR}
export GH_TOKEN=${GH_TOKEN}
export TRAVIS_REPO_SLUG=${TRAVIS_REPO_SLUG}
export GIT_EMAIL=${GIT_EMAIL}
export GIT_NAME=${GIT_NAME}

# ******************************************************************************
# Updating PyFunceble && Run PyFunceble
# Note: We use the same statement so that if something is broken everything else
#   is not run.
# ******************************************************************************
  sudo python3 ${TRAVIS_BUILD_DIR}/dev-tools/PyFunceble/PyFunceble.py --dev -u && \
  mv ${TRAVIS_BUILD_DIR}/dev-tools/PyFunceble/config_production.yaml ${TRAVIS_BUILD_DIR}/dev-tools/PyFunceble/config.yaml && \
  sudo python3 ${TRAVIS_BUILD_DIR}/dev-tools/PyFunceble/PyFunceble.py --travis -dbr 5 --cmd-before-end "bash ${TRAVIS_BUILD_DIR}/dev-tools/commit.sh" -a -ex --plain --split --share-logs --autosave-minutes 10 --commit-autosave-message "V0.1.${TRAVIS_BUILD_NUMBER} [PyFunceble]" --commit-results-message "V0.1.${TRAVIS_BUILD_NUMBER}" -f ${output}


fetch
initiate
prepare
#updatereadme
PyFunceble
#commit

# **********************
# Exit With Error Number
# **********************

exit ${?}


