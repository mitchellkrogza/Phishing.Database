#!/bin/bash
# Incremental Commit for Phishing Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

set -e
set -o pipefail

VERSIONNUMBER=$(date "+%F.%H")
LATESTBUILD="V.${VERSIONNUMBER}"

# *********************************************
# Get Travis CI Prepared for Committing to Repo
# *********************************************

UpdateFiles () {
# ****************************************
# Copy last tested files into root of repo
# ****************************************

domainstatuses="ACTIVE INACTIVE INVALID"
linkstatuses="ACTIVE INACTIVE INVALID"
todaystatus="ACTIVE"

for status in $(echo ${domainstatuses})
do
    statusFile="./phishing-domains/output/domains/${status}/list"

    if [[ -f ${statusFile} ]]
    then
        cat ${statusFile} | grep -v "^$" | grep -v "^#" > ./phishing-domains-${status}.txt
    else
        echo "" > ./phishing-domains-${status}.txt
    fi
done

for linkstatus in $(echo ${linkstatuses})
do
    linkstatusFile="./phishing-links/output/domains/${linkstatus}/list"

    if [[ -f ${linkstatusFile} ]]
    then
        cat ${linkstatusFile} | grep -v "^$" | grep -v "^#" > ./phishing-links-${linkstatus}.txt
    else
        echo "" > ./phishing-links-${linkstatus}.txt
    fi
done

for statusnow in $(echo ${todaystatus})
do
    statusnowFile="./phishing-links-last-hour/output/domains/${statusnow}/list"

    if [[ -f ${statusnowFile} ]]
    then
        cat ${statusnowFile} | grep -v "^$" | grep -v "^#" > ./phishing-links-${statusnow}-NOW.txt
    else
        echo "" > ./phishing-links-${statusnow}-NOW.txt
    fi
done

for statustoday in $(echo ${todaystatus})
do
    statustodayFile="./phishing-links-today/output/domains/${statustoday}/list"

    if [[ -f ${statustodayFile} ]]
    then
        cat ${statustodayFile} | grep -v "^$" | grep -v "^#" > ./phishing-links-${statustoday}-TODAY.txt
    else
        echo "" > ./phishing-links-${statustoday}-TODAY.txt
    fi
done

}

RunWhitelist () {
# *********************************************************
# Clean with whitelist
# *********************************************************

bash ./scripts/whitelist.sh

# *********************************************************
# Modify Readme File
# *********************************************************

bash ./scripts/modify-readme.sh
}


StripIPs () {
# STRIP FROM ACTIVE
grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" ./phishing-domains-ACTIVE.txt > ./phishing-IPs-ACTIVE.txt
sort -u ./phishing-IPs-ACTIVE.txt -o ./phishing-IPs-ACTIVE.txt
sort -u ./phishing-domains-ACTIVE.txt -o ./phishing-domains-ACTIVE.txt
grep -Fvxf ./phishing-IPs-ACTIVE.txt ./phishing-domains-ACTIVE.txt > ./phishing-domains-ACTIVEtmp.txt
mv ./phishing-domains-ACTIVEtmp.txt ./phishing-domains-ACTIVE.txt 
# STRIP FROM INACTIVE
grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" ./phishing-domains-INACTIVE.txt > ./phishing-IPs-INACTIVE.txt
sort -u ./phishing-IPs-INACTIVE.txt -o ./phishing-IPs-INACTIVE.txt
sort -u ./phishing-domains-INACTIVE.txt -o ./phishing-domains-INACTIVE.txt
grep -Fvxf ./phishing-IPs-INACTIVE.txt ./phishing-domains-INACTIVE.txt > ./phishing-domains-INACTIVEtmp.txt
mv ./phishing-domains-INACTIVEtmp.txt ./phishing-domains-INACTIVE.txt 
# STRIP FROM INVALID
grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" ./phishing-domains-INVALID.txt > ./phishing-IPs-INVALID.txt
sort -u ./phishing-IPs-INVALID.txt -o ./phishing-IPs-INVALID.txt
sort -u ./phishing-domains-INVALID.txt -o ./phishing-domains-INVALID.txt
grep -Fvxf ./phishing-IPs-INVALID.txt ./phishing-domains-INVALID.txt > ./phishing-domains-INVALIDtmp.txt
mv ./phishing-domains-INVALIDtmp.txt ./phishing-domains-INVALID.txt 
}

Compress () {
# TAR OUR INPUT FILES
echo "Delete old zip files"
rm ./input-source/ALL-feeds.zip
rm ./input-source/ALL-feeds-URLS.zip

echo "Compress Input Files"

zip -jrm ./input-source/ALL-feeds.zip ./input-source/ALL-feeds.lst
zip -jrm ./input-source/ALL-feeds-URLS.zip ./input-source/ALL-feeds-URLS.lst
ls -la ./input-source/

echo "Remove plain text files"
#rm ./input-source/ALL-feeds.lst
#rm ./input-source/ALL-feeds-URLS.lst
}

CommitData () {
          git config --global user.name "mitchellkrogza"
          git config --global user.email "mitchellkrog@gmail.com"
          git add -A
          git commit -m "${LATESTBUILD}"
          git push
}

UpdateFiles
StripIPs
RunWhitelist
Compress
CommitData

# **********************
# Exit With Error Number
# **********************

exit ${?}
