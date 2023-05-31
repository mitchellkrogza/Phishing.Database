---
name: False Positive
about: Reporting of any false positives or domains that need to be whitelisted
title: "[FALSE-POSITIVE]: "
labels: false positive
assignees: mitchellkrogza, funilrys
---

**Domains or links**
Please list any domains and links listed here which you believe are a false positive.

**More Information**
How did you discover your web site or domain was listed here?
1. Website was hacked
2. Incorrectly marked as Phishing on Phishtank or OpenPhish?

**Have you requested removal from other sources?**
Please include all relevant links to your existing removals / whitelistings.

**Additional context**
Add any other context about the problem here.

:exclamation:

We understand being listed on a Phishing Database like this can be frustrating and embarrassing for many web site owners. The first step is to remain calm. The second step is to rest assured one of our maintainers will address your issue as soon as possible. Please make sure you have provided as much information as possible to help speed up the process.

**Send a Pull Request for faster removal**
Users who understand github and creating Pull Requests can assist us for faster removals by sending a PR to the **mitchellkrogza/phishing** repository and add the FP domain one of the whitelists:
- `falsepositive.list` for a 1 to 1  match https://github.com/mitchellkrogza/phishing/blob/main/falsepositive.list
- `falsepositive_regex.list` matches against regex. https://github.com/mitchellkrogza/phishing/blob/main/falsepositive_regex.list
- `falsepositive_rzd.list` This list will tell the system to explicitly check for the given string plus all possible TLD. https://github.com/mitchellkrogza/phishing/blob/main/falsepositive_rzd.list

Please include the same information as above to help speed up the whitelisting process.

You should note that you should not expect merges are done in https://github.com/mitchellkrogza/phishing until the issue have been solved here, this is because those who can merge do not have access to the logs for why your domain got listed.

#### Open Source Project domain reporting tools
My Privacy DNS have 2 option for you to quickly add new phishing domains:

1. By using the web, support anonymously reporting: https://mypdns.eu.org/matrix/reporter/
2. By installing one of the cool Firefox add-ons, GUI, CLI tools: https://0xacab.org/my-privacy-dns/matrix/-/blob/master/tools/client_addon.md
