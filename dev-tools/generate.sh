#!/bin/bash
# Generator Script for Fail2Ban.WebExploits
# REPO: https://github.com/mitchellkrogza/Fail2Ban.WebExploits
# Copyright Mitchell Krog - mitchellkrog@gmail.com

tmplt=tmplt
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
#sudo mv ${outputtmp} ${output}
}

# *******************************
# Build the beginning of our file
# *******************************

generate () {
printf '%s\n' "# Fail2Ban Web Exploits Filter" >> ${tmplt}
printf '%s\n' "# Author & Copyright: Mitchell Krog - mitchellkrog@gmail.com" >> ${tmplt}
printf '%s\n' "# REPO: https://github.com/mitchellkrogza/Fail2Ban.WebExploits" >> ${tmplt}
printf '%s%s\n' "# " "${version}" >> ${tmplt}
printf '%s%s\n\n' "# Last Updated: " "${versiondate}" >> ${tmplt}
printf '%s\n' "[Definition]" >> ${tmplt}
printf '\n\n' >> ${tmplt}
printf '%s\n' "failregex = ^<HOST> -.*GET.*(/.git/config)" >> ${tmplt}

# **************************************************************
# Now loop through our input file and write the rest of the file
# **************************************************************

while IFS= read -r LINE
do
printf '%s%s%s%s\n' "            " "^<HOST> -.*GET.*(" "${LINE}" ")" >> ${tmplt}
done < ${input}

# *****************************
# Now write the end of our file
# *****************************

printf '\n%s\n' "ignoreregex ="  >> ${tmplt}

# *************************************
# Move the temp file to the output file
# *************************************

mv ${tmplt} ${output}

# *****************************************************
# Activate Dos2Unix to make sure file is in Unix format
# *****************************************************

dos2unix ${output}
}

# **************************************************
# Write Version and Exploit Count into the README.md
# **************************************************

updatereadme () {

printf '%s\n%s%s\n%s%s\n%s' "${startmarker}" "#### Version: " "${version}" "#### Total Exploits: " "${totalexploits}" "${endmarker}" >> ${tmprdme}
mv ${tmprdme} ${tmprdme2}
ed -s ${tmprdme2}<<\IN
1,/_______________/d
/____________________/,$d
,d
.r /home/travis/build/mitchellkrogza/Fail2Ban.WebExploits/README.md
/_______________/x
.t.
.,/____________________/-d
w /home/travis/build/mitchellkrogza/Fail2Ban.WebExploits/README.md
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

fetch
initiate
prepare
#generate
#updatereadme
commit

# **********************
# Exit With Error Number
# **********************

exit ${?}


