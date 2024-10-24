#!/bin/bash
# Modify README.md Script for Phishing.Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com 

set -e
set -o pipefail

tmprdme="./tmprdme"
tmprdme2="./tmprdme2"
testdate=$(date +%F)
testtime=$(date +%T)
timezone=$(date +%Z)
testday=$(date +%A)
testdate2=$(date +%D)
VERSIONNUMBER=$(date "+%F.%H")
version="V.${VERSIONNUMBER}"
startmarker="_______________"
endmarker="____________________"

# Get Last Modified Time of Test Results
#domainstested=$(git log -1 --pretty="format:%ci" ./phishing-domains/output/logs/)
#linkstested=$(git log -1 --pretty="format:%ci" ./phishing-links/output/logs/)
domainstested=$(cat ./phishing-domains/datetested)
linkstested=$(cat ./phishing-links/datetested)
echo ${domainstested}
echo ${linkstested}


# Domains Variables
activesites=$(wc -l < ./phishing-domains-ACTIVE.txt)
inactivesites=$(wc -l < ./phishing-domains-INACTIVE.txt)
invalidsites=$(wc -l < ./phishing-domains-INVALID.txt)
total=$((${activesites} + ${inactivesites} + ${invalidsites}))
totaldomains=$(wc -l < ./input-source/ALL-feeds.lst)
percentactive=$(awk "BEGIN { pc=100*${activesites}/${totaldomains}; i=int(pc); print (pc-i<0.5)?i:i+1 }")
percentinactive=$(awk "BEGIN { pc=100*${inactivesites}/${totaldomains}; i=int(pc); print (pc-i<0.5)?i:i+1 }")
percentinvalid=$(awk "BEGIN { pc=100*${invalidsites}/${totaldomains}; i=int(pc); print (pc-i<0.5)?i:i+1 }")


# Links Variables
activelinks=$(wc -l < ./phishing-links-ACTIVE.txt)
inactivelinks=$(wc -l < ./phishing-links-INACTIVE.txt)
invalidlinks=$(wc -l < ./phishing-links-INVALID.txt)
totallinks=$((${activelinks} + ${inactivelinks} + ${invalidlinks}))
totalurls=$(wc -l < ./input-source/ALL-feeds-URLS.lst)
percentactivelinks=$(awk "BEGIN { pc=100*${activelinks}/${totalurls}; i=int(pc); print (pc-i<0.5)?i:i+1 }")
percentinactivelinks=$(awk "BEGIN { pc=100*${inactivelinks}/${totalurls}; i=int(pc); print (pc-i<0.5)?i:i+1 }")
percentinvalidlinks=$(awk "BEGIN { pc=100*${invalidlinks}/${totalurls}; i=int(pc); print (pc-i<0.5)?i:i+1 }")

# Current Threats
activenow=$(wc -l < ./phishing-links-ACTIVE-NOW.txt)
activetoday=$(wc -l < ./phishing-links-ACTIVE-TODAY.txt)
discoveredtoday=$(wc -l < ./phishing-links-NEW-today.txt)


# Tar the Lists
cp ./input-source/ALL-feeds.lst ./ALL-phishing-domains.txt
cp ./input-source/ALL-feeds-URLS.lst ./ALL-phishing-links.txt
sudo tar -zcvf ./ALL-phishing-domains.tar.gz ./ALL-phishing-domains.txt
sudo tar -zcvf ./ALL-phishing-links.tar.gz ./ALL-phishing-links.txt
sudo rm ./ALL-phishing-domains.txt
sudo rm ./ALL-phishing-links.txt

# Get Full List Sizes
domainslistsize=$(du -h ./ALL-phishing-domains.tar.gz | awk '{print $1}')
urlslistsize=$(du -h ./ALL-phishing-links.tar.gz | awk '{print $1}')

# **************************************************
# Write Version and Exploit Count into the README.md
# **************************************************

updatereadme () {

printf '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' "${startmarker}" "#### Version: ${version}" "| :boom: Latest Threats<br/>@ ${testtime} | :boom: Active Threats<br/>${testday} ${testdate} | Total Links<br/>Discovered Today |" "| :---: | :---: |:---: |" "| :warning: [${activenow}](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-ACTIVE-NOW.txt) | :warning: [${activetoday}](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-ACTIVE-TODAY.txt) | [${discoveredtoday}](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-NEW-today.txt) |" "*****************************" "#### Total Phishing Domains Captured: [${totaldomains}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-domains.tar.gz) << (FILE SIZE: ${domainslistsize} tar.gz)" "#### Total Phishing Links Captured: [${totalurls}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-links.tar.gz) << (FILE SIZE: ${urlslistsize} tar.gz)" "${endmarker}" >> ${tmprdme}
mv ${tmprdme} ${tmprdme2}
ed -s ${tmprdme2}<<\IN
1,/_______________/d
/____________________/,$d
,d
.r ./README.md
/_______________/x
.t.
.,/____________________/-d
w ./README.md
q
IN
rm ${tmprdme2}
}

updatereadme


#OLD README UPDATE
#printf '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' "${startmarker}" "#### Version: ${version}" "| :boom: Latest Threats<br/>@ ${testtime} | :boom: Active Threats<br/>${testday} ${testdate} | Total Links<br/>Discovered Today |" "| :---: | :---: |:---: |" "| :warning: [${activenow}](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-ACTIVE-NOW.txt) | :warning: [${activetoday}](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-ACTIVE-TODAY.txt) | [${discoveredtoday}](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-NEW-today.txt) |" "*****************************" "| Phishing Domains Status  | Domain Count | Percentage | Last Tested | Download |" "| ---: | :---: | :---: | :---: |:---: |" "| ACTIVE <img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/green.jpg"/> | [${activesites}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt)  | ${percentactive} % | ${domainstested} | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt) |" "| INACTIVE <img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/red.jpg"/>  | [${inactivesites}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-INACTIVE.txt)  | ${percentinactive} % | ${domainstested} | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-INACTIVE.txt) |" "| INVALID <img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/blue.jpg"/> | [${invalidsites}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-INVALID.txt)  | ${percentinvalid} % | ${domainstested} | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-INVALID.txt) |" "*****************************" "| &emsp;&ensp;Phishing Links Status | &emsp;Link Count &ensp; | Percentage | Last Tested | Download |" "| ---: | :---: | :---: | :---: |:---: |" "| ACTIVE <img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/green.jpg"/> | [${activelinks}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ACTIVE.txt)  | ${percentactivelinks} % | ${linkstested} | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ACTIVE.txt) |" "| INACTIVE <img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/red.jpg"/>  | [${inactivelinks}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-INACTIVE.txt)  | ${percentinactivelinks} % | ${linkstested} | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-INACTIVE.txt) |" "| INVALID <img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/blue.jpg"/> | [${invalidlinks}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-INVALID.txt)  | ${percentinvalidlinks} % | ${linkstested} | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-INVALID.txt) |" "*****************************" "#### Total Phishing Domains Captured: [${totaldomains}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-domains.tar.gz) << (FILE SIZE: ${domainslistsize} tar.gz)" "#### Total Phishing Links Captured: [${totalurls}](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-links.tar.gz) << (FILE SIZE: ${urlslistsize} tar.gz)" "${endmarker}" >> ${tmprdme}



exit ${?}

