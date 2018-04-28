#!/bin/bash
# Generator Script for Phishing.Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

# *******************************
# Input and Output File Variables
# *******************************

input1=${TRAVIS_BUILD_DIR}/input-source/openphish-feed.list
input2=${TRAVIS_BUILD_DIR}/input-source/illegalfawn-feed.list
output=${TRAVIS_BUILD_DIR}/dev-tools/phishing-domains-ALL.list
#output2=${TRAVIS_BUILD_DIR}/dev-tools/phishing-domains-IDNA.list

# **************
# Temp Variables
# **************

outputtmp=${TRAVIS_BUILD_DIR}/phishing.tmp
feed1=${TRAVIS_BUILD_DIR}/input-source/openphish.list
tmp=${TRAVIS_BUILD_DIR}/input-source/tmp.list

# **********************************************
# Fetch our feed(s) and append to our input file
# **********************************************

fetch () {
sudo wget https://hosts.ubuntu101.co.za/openphish/openphish-feed.list -O ${feed1}
cat ${feed1} >> ${input1}
sudo rm ${feed1}
}

# *************************************************
# Prepare our input lists and remove any duplicates
# *************************************************

initiate () {

# Prepare Feed 1
sort -u ${input1} -o ${input1}
grep '[^[:blank:]]' < ${input1} > ${tmp}
sudo mv ${tmp} ${input1}

# Prepare Feed 2
sort -u ${input2} -o ${input2}
grep '[^[:blank:]]' < ${input2} > ${tmp}
sudo mv ${tmp} ${input2}

}

# ***************************************
# Prepare our list for PyFunceble Testing
# ***************************************

prepare () {
sudo truncate -s 0 ${output}
sudo cp ${input1} ${output}
cat ${input2} >> ${output}
cut -d'/' -f3 ${output} > ${outputtmp}
sort -u ${outputtmp} -o ${outputtmp}
grep '[^[:blank:]]' < ${outputtmp} > ${output}
sudo rm ${outputtmp}
dos2unix ${output}
}


# *********************************
# Prepare our list into IDNA format
# *********************************

idna () {
domain2idna -f ${output} -o ${tmp}
sudo mv ${tmp} ${output}
}

fetch
initiate
prepare
idna


# **********************
# Exit With Error Number
# **********************

exit ${?}


