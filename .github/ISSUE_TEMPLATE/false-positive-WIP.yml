name: False Positive
title: "[FALSE-POSITIVE]: "
description: |
  Reporting of any false positives or domains that need to be whitelisted
labels: ["false positive"]
assignees:
  - mitchellkrogza
  - funilrys
body:
  - type: markdown
    attributes:
      value: "## Domains or links"
  - type: markdown
    attributes:
      value: |
        Please list any domains and links listed here which you believe
        are a false positive.

  - type: checkboxes
    id: source
    attributes:
      label: "## More Information"
      description: |
        How did you discover your web site or domain was listed here?
      options:
        - label: Website was hacked
          required: true
        - label: Phishtank
        - label: OpenPhish
        - label: VirusTotal
        - label: Other

  - type: textarea
    id: ifOther
    attributes:
      label: If other
      description: Please tell us where you have requested whitelisting from
      value: |
        1. My Privacy DNS
        2. EasyList
        3. F-Secure
      render: text

  - type: textarea
    id: removal
    attributes:
      label: "## Have you requested removal from other sources?"
      description: |
        Please include all relevant links to your existing
        removals / whitelistings.
      value: |
        1. example.org
        2. example.com
        3, example.net
      render: txt
      
  - type: markdown
    attributes:
      value: "## Additional context"
  - type: markdown
    attributes:
      value: Add any other context about the problem here.

  - type: markdown
    attributes:
      value: |
        We understand being listed on a Phishing Database like this can be
        frustrating and embarrassing for many web site owners. The first
        step is to remain calm. The second step is to rest assured one of
        our maintainers will address your issue as soon as possible.
        Please make sure you have provided as much information as possible
        to help speed up the process.

  - type: markdown
    attributes:
      value: "## Send a Pull Request for faster removal"

  - type: markdown
    attributes:
      value: |
        Users who understand github and creating Pull Requests can assist us
        for faster removals by sending a PR to the **mitchellkrogza/phishing**
        repository and add the FP domain one of the whitelists:
        - `falsepositive.list` for a 1 to 1  match
          https://github.com/mitchellkrogza/phishing/blob/main/falsepositive.list
        - `falsepositive_regex.list` matches against regex.
          https://github.com/mitchellkrogza/phishing/blob/main/falsepositive_regex.list
        - `falsepositive_rzd.list` This list will tell the system to explicitly
          check for the given string plus all possible TLD.
          https://github.com/mitchellkrogza/phishing/blob/main/falsepositive_rzd.list

        Please include the same information as above to help speed up the
        whitelisting process.

        You should note that you should not expect merges are done in
        https://github.com/mitchellkrogza/phishing until the issue have
        been solved here, this is because those who can merge do not have
        access to the logs for why your domain got listed.

  - type: markdown
    attributes:
      value: "#### Open Source Project domain reporting tools"
  - type: markdown
    attributes:
      value: |
        My Privacy DNS have 2 option for you to quickly add new phishing domains:

        1. By using the web, support anonymously reporting:
           https://mypdns.eu.org/matrix/reporter/
        2. By installing one of the cool Firefox add-ons, GUI, CLI tools:
           https://0xacab.org/my-privacy-dns/matrix/-/blob/master/tools/client_addon.md
