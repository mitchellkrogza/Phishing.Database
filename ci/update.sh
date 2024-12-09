#!/usr/bin/env bash

# The ci/cd updater for the Phishing.Database project.
#
# MIT License
# Copyright (c) 2018-2024 Mitchell Krog - github.com/mitchellkrogza
# Copyright (c) 2018-2024 Nissar Chababy - github.com/funilrys

# Uncomment for debugging.
#set -x
# Stop on first missing variable.
set -u
# Stop on first error.
set -e

# Check if dos2unix is installed.
hash dos2unix
# Check if zip is installed.
hash zip
# Check if unzip is installed.
hash unzip
# Check if sort is installed.
hash sort
# Check if awk is installed.
hash awk
# Check if nproc is installed.
hash nproc

# The work directory of the project.
export ciDir="$(realpath $(dirname ${0}))"
export workDir="$(dirname ${ciDir})"

# A file where we put variables.
loadEnvFile="${ciDir}/.loadenv"
# A file where our helpers are located.
loadHelpersFile="${ciDir}/.loadhelpers"

if [[ -f "${loadHelpersFile}" ]]; then
    source "${loadHelpersFile}"
else
    echo "File not found: ${loadHelpersFile}"
    exit 1
fi

if [[ -f "${loadEnvFile}" ]]; then
    source "${loadEnvFile}"
fi

# A function that updates and renames some of our files.
#
# Usage: migrateFileStructure
function migrateFileStructure() {
    printTitle "Migrating file structure"
    if [[ -f "${LEGACY_INPUT_DOMAINS_FILE}" ]]
    then
        cd ${DOMAINS_SOURCE_DIR}

        mv "${LEGACY_INPUT_DOMAINS_FILE}" "${INPUT_DOMAINS_FILE}"
        ln -s "$(basename ${INPUT_DOMAINS_FILE})" "$(basename ${LEGACY_INPUT_DOMAINS_FILE})"

        cd ${workDir}
    fi

    if [[ -f "${LEGACY_INPUT_URLS_FILE}" ]]
    then
        cd ${URLS_SOURCE_DIR}

        mv "${LEGACY_INPUT_URLS_FILE}" "${INPUT_URLS_FILE}"
        ln -s "$(basename ${INPUT_URLS_FILE})" "$(basename ${LEGACY_INPUT_URLS_FILE})"

        cd ${workDir}
    fi

    rm -f "${LEGACY_PHISHING_LINKS_ACTIVE_TODAY_FILE}"
}

# A function that import data from our other repository.
#
# Usage: importExtraData
function fetchExtraData() {
    printTitle "Fetching extra data"
    local whitelistMeDestination="${TEMP_DIR}/whitelist.list"
    local whitelistMeRegexDestionation="${TEMP_DIR}/whitelist-regex.list"
    local whitelistMeRZDDestination="${TEMP_DIR}/whitelist-rzd.list"

    local additionalWildcardDestination="${TEMP_DIR}/whitelist-wildcard.list"
    local additionalDomainDestination="${TEMP_DIR}/add-domain"
    local additionalLinkDestination="${TEMP_DIR}/add-link"

    # Download the false positive list.
    curl -sfL "https://github.com/mitchellkrogza/phishing/raw/main/falsepositive.list" -o "${whitelistMeDestination}"
    # Download the false positive regex list.
    curl -sfL "https://github.com/mitchellkrogza/phishing/raw/main/falsepositive_regex.list" -o "${whitelistMeRegexDestionation}"
    # Download the false positive rzd list.
    curl -sfL "https://github.com/mitchellkrogza/phishing/raw/main/falsepositive_rzd.list" -o "${whitelistMeRZDDestination}"
    # Download the additional wildcard data.
    curl -sfL "https:/github.com/mitchellkrogza/phishing/raw/main/add-wildcard-domain" -o "${additionalWildcardDestination}"
    # Download the additional domains data.
    curl -sfL "https://github.com/mitchellkrogza/phishing/raw/main/add-domain" -o "${additionalDomainDestination}"
    # Download the additional links data.
    curl -sfL "https://github.com/mitchellkrogza/phishing/raw/main/add-link" -o "${additionalLinkDestination}"

    # Merge the false positive list with the local whitelist.
    cat "${whitelistMeDestination}" >> "${WHITELIST_ME_FILE}"
    # Merge the false positive regex list with the local whitelist.
    cat "${whitelistMeRegexDestionation}" >> "${WHITELIST_ME_REGEX_FILE}"
    # Merge the false positive RZD list with the local whitelist.
    cat "${whitelistMeRZDDestination}" >> "${WHITELIST_ME_RZD_FILE}"
    # Merge the additional data into the input-sources.
    cat "${additionalWildcardDestination}" >> "${INPUT_DOMAINS_FILE}"
    # Merge the additional data into the input-sources.
    cat "${additionalDomainDestination}" >> "${INPUT_DOMAINS_FILE}"
    # Merge the additional data into the input-sources.
    cat "${additionalLinkDestination}" >> "${INPUT_URLS_FILE}"

    # Cleanup the temporary files.
    rm -f "${whitelistMeDestination}"
    rm -f "${whitelistMeRegexDestionation}"
    rm -f "${whitelistMeRZDDestination}"
    rm -f "${additionalDomainDestination}"
    rm -f "${additionalLinkDestination}"

}

# A function that unpacks the input files.
#
# Usage: unpackInputFiles
function unpackInputFiles() {
    printTitle "Unpacking input files"

    unzip -o "${PHISHING_ALL_FEEDS_DOMAINS_ZIP}" -d "${INPUT_SOURCE_DIR}"
    unzip -o "${PHISHING_ALL_FEEDS_LINKS_ZIP}" -d "${INPUT_SOURCE_DIR}"

    ls -la "${INPUT_SOURCE_DIR}"
}

# A function that prepares the files before we start the processing them.
#
# Usage: prepareFiles
function prepareFiles() {
    echo "dos2unix the files"
    dos2unix "${WHITELIST_ME_FILE}"
    dos2unix "${WHITELIST_ME_REGEX_FILE}"
    dos2unix "${WHITELIST_ME_RZD_FILE}"
    dos2unix "${INPUT_DOMAINS_FILE}"
    dos2unix "${INPUT_URLS_FILE}"

    echo "Cleaning up the files"
    stripBinaryChars "${WHITELIST_ME_FILE}"
    stripBinaryChars "${WHITELIST_ME_REGEX_FILE}"
    stripBinaryChars "${WHITELIST_ME_RZD_FILE}"
    stripBinaryChars "${INPUT_DOMAINS_FILE}"
    stripBinaryChars "${INPUT_URLS_FILE}"

    echo "Sorting the files"
    sort -u "${WHITELIST_ME_FILE}" -o "${WHITELIST_ME_FILE}"
    sort -u "${WHITELIST_ME_REGEX_FILE}" -o "${WHITELIST_ME_REGEX_FILE}"
    sort -u "${WHITELIST_ME_RZD_FILE}" -o "${WHITELIST_ME_RZD_FILE}"
    sort -u "${INPUT_DOMAINS_FILE}" -o "${INPUT_DOMAINS_FILE}"
    sort -u "${INPUT_URLS_FILE}" -o "${INPUT_URLS_FILE}"
}

# A function that applies all our whitelists to all datasets.
#
# Usage: applyWhitelist
function applyWhitelist() {
    printTitle "Applying whitelist"

    local inputDomainsFile=(
        "${PHISHING_DOMAINS_ACTIVE_FILE}"
        "${PHISHING_DOMAINS_INACTIVE_FILE}"
        "${PHISHING_DOMAINS_INVALID_FILE}"
        "${PHISHING_DOMAINS_NEW_TODAY_FILE}"
        "${PHISHING_DOMAINS_ACTIVE_TODAY_FILE}"
        "${PHISHING_ALL_FEEDS_DOMAINS_FILE}"
    )

    local outputDomainsFile=(
        "${PHISHING_DOMAINS_ACTIVE_FILE}"
        "${PHISHING_DOMAINS_INACTIVE_FILE}"
        "${PHISHING_DOMAINS_INVALID_FILE}"
        "${PHISHING_DOMAINS_NEW_TODAY_FILE}"
        "${PHISHING_DOMAINS_ACTIVE_TODAY_FILE}"
        "${PHISHING_ALL_DOMAINS_FILE}"
    )

    local inputLinksFile=(
        "${PHISHING_LINKS_ACTIVE_FILE}"
        "${PHISHING_LINKS_INACTIVE_FILE}"
        "${PHISHING_LINKS_INVALID_FILE}"
        "${PHISHING_LINKS_NEW_TODAY_FILE}"
        "${PHISHING_LINKS_ACTIVE_TODAY_FILE}"
        "${PHISHING_ALL_FEEDS_LINKS_FILE}"
    )

    local outputLinksFile=(
        "${PHISHING_LINKS_ACTIVE_FILE}"
        "${PHISHING_LINKS_INACTIVE_FILE}"
        "${PHISHING_LINKS_INVALID_FILE}"
        "${PHISHING_LINKS_NEW_TODAY_FILE}"
        "${PHISHING_LINKS_ACTIVE_TODAY_FILE}"
        "${PHISHING_ALL_LINKS_FILE}"
    )

    for index in "${!inputDomainsFile[@]}"
    do
        if [[ ! -f "${inputDomainsFile[index]}" ]]
        then
            continue
        fi

        echo "Whitelisting ${inputDomainsFile[index]} into ${outputDomainsFile[index]}"
        uhb_whitelist -m -p "${CPU_COUNT}" -wc -f "${inputDomainsFile[index]}" -o "${outputDomainsFile[index]}" --reg "${WHITELIST_ME_REGEX_FILE}" --rzd "${WHITELIST_ME_RZD_FILE}" -w "${WHITELIST_ME_FILE}" ${EXTRAS_WHITELIST_SOURCES}
        echo "Whitelisted ${inputDomainsFile[index]} into ${outputDomainsFile[index]}"

        echo ""

        echo "Cleaning up ${outputDomainsFile[index]}"

        # Ensure that lines without dots are removed.
        awk -i inplace '/\./' "${outputDomainsFile[index]}"
        # Remove blank lines.
        awk -i inplace 'NF > 0' "${outputDomainsFile[index]}"
        # Just in case, dos2unix the file.
        dos2unix "${outputDomainsFile[index]}"
        # Just in case, remove any binary characters.
        stripBinaryChars "${outputDomainsFile[index]}"
        # Just in case, sort the file.
        sort -u "${outputDomainsFile[index]}" -o "${outputDomainsFile[index]}"

        echo "Cleaned up ${outputDomainsFile[index]}"
        echo ""
    done
}

# A function that moves the status files to the correct location.
#
# Usage: moveStatusFiles
function moveStatusFiles() {
    local statuses=(
        "ACTIVE"
        "INACTIVE"
        "INVALID"
    )

    for status in "${statuses[@]}"
    do
        local domainsSourceFile="${DOMAINS_STATUS_DIR}/${status}"
        local domainsDestinationFile="phishing-domains-${status}.txt"

        local linksSourceFile="${URLS_STATUS_DIR}/${status}"
        local linksDestinationFile="phishing-links-${status}.txt"

        local ipsSourceFile="${DOMAINS_STATUS_DIR}/IPs-${status}"
        local ipsDestinationFile="phishing-IPs-${status}.txt"

        if [[ -f "${domainsSourceFile}" ]]
        then
            cp "${domainsSourceFile}" "${domainsDestinationFile}"
        fi

        if [[ -f "${linksSourceFile}" ]]
        then
            cp "${linksSourceFile}" "${linksDestinationFile}"
        fi

        if [[ -f "${ipsSourceFile}" ]]
        then
            cp "${ipsSourceFile}" "${ipsDestinationFile}"
        fi
    done
}

# A function that format the ACTIVE file into an AdBlock compatible format.
#
# Usage: convertAdBlock
function convertAdBlock() {
    printTitle "Converting to AdBlock format"

    if [[ -f "${PHISHING_DOMAINS_ACTIVE_FILE}" ]]
    then
        echo "Converting ${PHISHING_DOMAINS_ACTIVE_FILE} to AdBlock format"
        cat "${CI_ADBLOCK_HEADER_TEMPLATE}" > "${PHISHING_DOMAINS_ACTIVE_ADBLOCK_FILE}"

        awk '{ print "||" $0 "^" }' "${PHISHING_DOMAINS_ACTIVE_FILE}" >> "${PHISHING_DOMAINS_ACTIVE_ADBLOCK_FILE}"
    fi
}

# A function that compresses the new version of the files.
#
# Usage: compressFiles
function compressFiles() {
    printTitle "Compressing files"

    # Cleanup the previous versions.
    rm -f "${PHISHING_ALL_FEEDS_DOMAINS_ZIP}"
    rm -f "${PHISHING_ALL_FEEDS_LINKS_ZIP}"
    rm -f "${PHISHING_ALL_DOMAINS_TGZ}"
    rm -f "${PHISHING_ALL_LINKS_TGZ}"

    zip -j "${PHISHING_ALL_FEEDS_DOMAINS_ZIP}" "${PHISHING_ALL_FEEDS_DOMAINS_FILE}"
    zip -j "${PHISHING_ALL_FEEDS_LINKS_ZIP}" "${PHISHING_ALL_FEEDS_LINKS_FILE}"

    cp "${PHISHING_ALL_FEEDS_DOMAINS_FILE}" "${PHISHING_ALL_DOMAINS_FILE}"
    cp "${PHISHING_ALL_FEEDS_LINKS_FILE}" "${PHISHING_ALL_LINKS_FILE}"

    tar -zcvf "${PHISHING_ALL_DOMAINS_TGZ}" "${PHISHING_ALL_FEEDS_DOMAINS_FILE}"
    tar -zcvf "${PHISHING_ALL_LINKS_TGZ}" "${PHISHING_ALL_FEEDS_LINKS_FILE}"
}

# A function taht updates the README file.
#
# Usage: updateReadme
function updateReadme() {
    printTitle "Updating README"

    local testDate="$(date +%F)"
    local testDay="$(date +%A)"
    local testTime="$(date +%T)"
    local timeZone="$(date +%Z)"

    local activeNowCount="0"
    local activeTodayCount="0"
    local discoveredTodayCount="0"
    local domainsCount="$(wc -l ${PHISHING_ALL_FEEDS_DOMAINS_FILE} | awk '{ print $1 }')"
    local linksCount="$(wc -l ${PHISHING_ALL_FEEDS_LINKS_FILE} | awk '{ print $1 }')"

    local domainsTGZSize="$(du -h ${PHISHING_ALL_DOMAINS_TGZ} | awk '{ print $1 }')"
    local linksTGZSize="$(du -h ${PHISHING_ALL_LINKS_TGZ} | awk '{ print $1 }')"

    cat "${CI_README_TEMPLATE}" | sed "s|%%version%%|${BUILD_NUMBER}|g" | \
        sed "s|%%testTime%%|${testTime}|g" | \
        sed "s|%%testDay%%|${testDay}|g" | \
        sed "s|%%testDate%%|${testDate}|g" | \
        sed "s|%%activeNowCount%%|${activeNowCount}|g" | \
        sed "s|%%activeTodayCount%%|${activeTodayCount}|g" | \
        sed "s|%%discoveredTodayCount%%|${discoveredTodayCount}|g" | \
        sed "s|%%domainsCount%%|${domainsCount}|g" | \
        sed "s|%%linksCount%%|${linksCount}|g" | \
        sed "s|%%domainsTGZSize%%|${domainsTGZSize}|g" | \
        sed "s|%%linksTGZSize%%|${linksTGZSize}|g" > "${README_FILE}"
}

# A function that cleanup the unneeded files.
#
# Usage: cleanupFiles
function cleanupFiles() {
    # We now remove the original files.
    rm -f "${PHISHING_ALL_FEEDS_DOMAINS_FILE}"
    rm -f "${PHISHING_ALL_FEEDS_LINKS_FILE}"
    rm -f "${PHISHING_ALL_DOMAINS_FILE}"
    rm -f "${PHISHING_ALL_LINKS_FILE}"
}

# Unpack the input files.
unpackInputFiles
# Fetch extra data.
fetchExtraData
# Prepare the files.
prepareFiles
# Move the status files.
moveStatusFiles
# Apply the whitelist.
applyWhitelist
# Convert to AdBlock format.
convertAdBlock
# Compress the files.
compressFiles
# Update the README file.
updateReadme
# Cleanup the files.
cleanupFiles
# Ensure that git is configured.
setupGit
# push data.
pushData