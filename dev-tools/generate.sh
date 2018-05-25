#!/bin/bash
# Generator Script for Phishing.Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

input=${TRAVIS_BUILD_DIR}/dev-tools/phishing-domains-IDNA.list

# *********************************************
# Get Travis CI Prepared for Committing to Repo
# *********************************************

PrepareTravis () {
    git remote rm origin
    git remote add origin https://${GH_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git
    git config --global user.email "${GIT_EMAIL}"
    git config --global user.name "${GIT_NAME}"
    git config --global push.default simple
    git checkout master
}

# **********************
# Run PyFunceble Testing
# **********************************************************
# Find PyFunceble at: https://github.com/funilrys/PyFunceble
# **********************************************************

PyFunceble () {

    yeartag=$(date +%Y)
    monthtag=$(date +%m)
    sudo chown -R travis:travis ${TRAVIS_BUILD_DIR}/
    sudo chmod +x ${TRAVIS_BUILD_DIR}/dev-tools/PyFunceble/PyFunceble.py
    cd ${TRAVIS_BUILD_DIR}/dev-tools

    # We use the following so that PyFunceble will get and configure automatically everything needed.
    export PYFUNCEBLE_AUTO_CONFIGURATION="PyFunceble"

    PyFunceble --travis -dbr 5 --cmd-before-end "bash ${TRAVIS_BUILD_DIR}/dev-tools/commit.sh" -ex --plain --autosave-minutes 10 --commit-autosave-message "V0.1.${TRAVIS_BUILD_NUMBER} [PyFunceble]" --commit-results-message "V0.1.${TRAVIS_BUILD_NUMBER}" -f ${input}

}

PrepareTravis
PyFunceble

# **********************
# Exit With Error Number
# **********************

exit ${?}
