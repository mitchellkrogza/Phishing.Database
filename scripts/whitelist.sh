#!/bin/bash
# Whitelist Script for Phishing.Database
# Contributed by Alex Williams - https://github.com/mkb2091

set -e
set -o pipefail

# UNTAR INPUT FILES
#cd ./input-source/
#ls -la
unzip ./input-source/ALL-feeds.zip -d ./input-source/
unzip ./input-source/ALL-feeds-URLS.zip -d ./input-source/
ls -la ./input-source/

# Sort Lists
sort -u ./whitelist.me/whitelist.me -o ./whitelist.me/whitelist.me
sort -u ./whitelist.anti/whitelist.anti -o ./whitelist.anti/whitelist.anti

# WhiteList Domains
uhb_whitelist -f ./phishing-domains-ACTIVE.txt -o ./phishing-domains-ACTIVE.txt -w ./whitelist.me/whitelist.me
uhb_whitelist -f ./phishing-domains-INACTIVE.txt -o ./phishing-domains-INACTIVE.txt -w ./whitelist.me/whitelist.me
uhb_whitelist -f ./phishing-domains-INVALID.txt -o ./phishing-domains-INVALID.txt -w ./whitelist.me/whitelist.me
uhb_whitelist -f ./input-source/ALL-feeds.lst -o ./ALL-phishing-domains.txt -w ./whitelist.me/whitelist.me

# WhiteList Links
uhb_whitelist -f ./phishing-links-ACTIVE.txt -o ./phishing-links-ACTIVE.txt --anti-whitelist ./whitelist.anti/whitelist.anti -w ./whitelist.me/whitelist.me
uhb_whitelist -f ./phishing-links-INACTIVE.txt -o ./phishing-links-INACTIVE.txt --anti-whitelist ./whitelist.anti/whitelist.anti -w ./whitelist.me/whitelist.me
uhb_whitelist -f ./phishing-links-INVALID.txt -o ./phishing-links-INVALID.txt --anti-whitelist ./whitelist.anti/whitelist.anti -w ./whitelist.me/whitelist.me
uhb_whitelist -f ./input-source/ALL-feeds-URLS.lst -o ./ALL-phishing-links.txt --anti-whitelist ./whitelist.anti/whitelist.anti -w ./whitelist.me/whitelist.me

# FIX Remove Orphaned Domains - Lines not containing a . 
cat ./phishing-domains-ACTIVE.txt | sed '/\./!d' > ./phishing-domains-ACTIVE.tmp && mv ./phishing-domains-ACTIVE.tmp ./phishing-domains-ACTIVE.txt
cat ./phishing-domains-INACTIVE.txt | sed '/\./!d' > ./phishing-domains-INACTIVE.tmp && mv ./phishing-domains-INACTIVE.tmp ./phishing-domains-INACTIVE.txt



# **********************
# Exit With Error Number
# **********************

exit ${?}

