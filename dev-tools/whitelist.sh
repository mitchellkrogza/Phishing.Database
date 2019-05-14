uhb_whitelist -f phishing-domains-ACTIVE-in-testing.txt -o phishing-domains-ACTIVE-in-testingTEMP.txt
uhb_whitelist -f phishing-domains-ACTIVE.txt -o phishing-domains-ACTIVETEMP.txt
uhb_whitelist -f phishing-domains-INACTIVE-in-testing.txt -o phishing-domains-INACTIVE-in-testingTEMP.txt
uhb_whitelist -f phishing-domains-INACTIVE.txt -o phishing-domains-INACTIVETEMP.txt
uhb_whitelist -f phishing-domains-INVALID-in-testing.txt -o phishing-domains-INVALID-in-testingTEMP.txt
uhb_whitelist -f phishing-domains-INVALID.txt -o phishing-domains-INVALIDTEMP.txt
mv phishing-domains-ACTIVE-in-testingTEMP.txt phishing-domains-ACTIVE-in-testing.txt
mv phishing-domains-ACTIVETEMP.txt phishing-domains-ACTIVE.txt
mv phishing-domains-INACTIVE-in-testingTEMP.txt phishing-domains-INACTIVE-in-testing.txt
mv phishing-domains-INACTIVETEMP.txt phishing-domains-INACTIVE.txt
mv phishing-domains-INVALID-in-testingTEMP.txt phishing-domains-INVALID-in-testing.txt
mv phishing-domains-INVALIDTEMP.txt phishing-domains-INVALID.txt
