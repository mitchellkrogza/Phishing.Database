#!/bin/bash
# Generator Script for Phishing.Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

input=${TRAVIS_BUILD_DIR}/dev-tools/phishing-domains-ALL.lst
pyfuncebleConfigurationFileLocation=${TRAVIS_BUILD_DIR}/dev-tools/.PyFunceble.yaml
pyfuncebleProductionConfigurationFileLocation=${TRAVIS_BUILD_DIR}/dev-tools/.PyFunceble_production.yaml


# **********************
# Run PyFunceble Testing
# **********************************************************
# Find PyFunceble at: https://github.com/funilrys/PyFunceble
# **********************************************************

RunFunceble () {

    yeartag=$(date +%Y)
    monthtag=$(date +%m)

    cd ${TRAVIS_BUILD_DIR}/dev-tools

    hash PyFunceble

    if [[ -f "${pyfuncebleConfigurationFileLocation}" ]]
    then
        rm "${pyfuncebleConfigurationFileLocation}"
        rm "${pyfuncebleProductionConfigurationFileLocation}"
    fi

    PyFunceble --travis --idna -ex --dns 1.1.1.1 1.0.0.1 --cmd "bash ${TRAVIS_BUILD_DIR}/dev-tools/incremental-commit.sh" --cmd-before-end "bash ${TRAVIS_BUILD_DIR}/dev-tools/commit.sh" --plain --autosave-minutes 20 --commit-autosave-message "V1.0.${TRAVIS_BUILD_NUMBER} [PyFunceble]" --commit-results-message "V1.0.${TRAVIS_BUILD_NUMBER}" -f ${input}

}

RunFunceble

# DEBUGGING COMMITS - Just Disable RunFunceble Function and Enable DebugCommit function
DebugCommit () {
    bash ${TRAVIS_BUILD_DIR}/dev-tools/modify-readme.sh
    bash ${TRAVIS_BUILD_DIR}/dev-tools/debug-commit.sh
}

#DebugCommit

# **********************
# Exit With Error Number
# **********************

exit ${?}
