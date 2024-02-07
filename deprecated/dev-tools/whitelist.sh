#!/bin/bash
# Whitelist Script for Phishing.Database
# Contributed by Alex Williams - https://github.com/mkb2091

set -e

# Sort Lists
sort -u ${TRAVIS_BUILD_DIR}/whitelist.me/whitelist.me -o ${TRAVIS_BUILD_DIR}/whitelist.me/whitelist.me
sort -u ${TRAVIS_BUILD_DIR}/whitelist.anti/whitelist.anti -o ${TRAVIS_BUILD_DIR}/whitelist.anti/whitelist.anti

# WhiteList Domains
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt -w ${TRAVIS_BUILD_DIR}/whitelist.me/whitelist.me
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt -w ${TRAVIS_BUILD_DIR}/whitelist.me/whitelist.me
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt -w ${TRAVIS_BUILD_DIR}/whitelist.me/whitelist.me
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/input-source/ALL-feeds.lst -o ${TRAVIS_BUILD_DIR}/ALL-phishing-domains.txt -w ${TRAVIS_BUILD_DIR}/whitelist.me/whitelist.me

# WhiteList Links
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-links-ACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-links-ACTIVE.txt --anti-whitelist ${TRAVIS_BUILD_DIR}/whitelist.anti/whitelist.anti -w ${TRAVIS_BUILD_DIR}/whitelist.me/whitelist.me
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-links-INACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-links-INACTIVE.txt --anti-whitelist ${TRAVIS_BUILD_DIR}/whitelist.anti/whitelist.anti -w ${TRAVIS_BUILD_DIR}/whitelist.me/whitelist.me
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-links-INVALID.txt -o ${TRAVIS_BUILD_DIR}/phishing-links-INVALID.txt --anti-whitelist ${TRAVIS_BUILD_DIR}/whitelist.anti/whitelist.anti -w ${TRAVIS_BUILD_DIR}/whitelist.me/whitelist.me
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/input-source/ALL-feeds-URLS.lst -o ${TRAVIS_BUILD_DIR}/ALL-phishing-links.txt --anti-whitelist ${TRAVIS_BUILD_DIR}/whitelist.anti/whitelist.anti -w ${TRAVIS_BUILD_DIR}/whitelist.me/whitelist.me

# FIX Remove Orphaned Domains - Lines not containing a . 
cat ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt | sed '/\./!d' > ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.tmp && mv ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.tmp ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt
cat ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt | sed '/\./!d' > ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.tmp && mv ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.tmp ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt


# **********************
# Exit With Error Number
# **********************

exit ${?}

