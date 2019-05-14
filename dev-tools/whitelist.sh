uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE-in-testing.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE-in-testing.txt -m -p 60
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-ACTIVE.txt -m -p 60
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE-in-testing.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE-in-testing.txt -m -p 60
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INACTIVE.txt -m -p 60
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID-in-testing.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID-in-testing.txt -m -p 60
uhb_whitelist -f ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt -o ${TRAVIS_BUILD_DIR}/phishing-domains-INVALID.txt -m -p 60

