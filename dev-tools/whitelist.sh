uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE-in-testing.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE-in-testingTEMP.txt
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVETEMP.txt
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE-in-testing.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE-in-testingTEMP.txt
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVETEMP.txt
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID-in-testing.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID-in-testingTEMP.txt
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INVALIDTEMP.txt
mv ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE-in-testingTEMP.txt ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE-in-testing.txt
mv ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVETEMP.txt ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt
mv ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE-in-testingTEMP.txt ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE-in-testing.txt
mv ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVETEMP.txt ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt
mv ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID-in-testingTEMP.txt ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID-in-testing.txt
mv ${TRAVIS_BUILD_DIR}/phishing-domains-INVALIDTEMP.txt ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt
