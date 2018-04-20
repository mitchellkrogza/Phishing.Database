#!/bin/bash
# Commit Script for Phishing.Database
# REPO: https://github.com/mitchellkrogza/Phishing.Database
# Copyright Mitchell Krog - mitchellkrog@gmail.com

sudo chown -R travis:travis ${TRAVIS_BUILD_DIR}/

sudo chmod +x ${TRAVIS_BUILD_DIR}/.dev-tools/pulldata.sh
sudo chmod +x ${TRAVIS_BUILD_DIR}/.dev-tools/modify-readme.sh

sudo ${TRAVIS_BUILD_DIR}/.dev-tools/pulldata.sh
sudo ${TRAVIS_BUILD_DIR}/.dev-tools/modify-readme.sh

exit ${?}


