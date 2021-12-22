name: False Positive Report
description: Reporting of any false positives or domains that need to be whitelisted
labels: ["False Positive"]
assignees:
  - mitchellkrogza
  - funilrys
body:
  - type: markdown
    attributes:
      value: |
        We understand being listed on a Phishing Database like this can
        be frustrating and embarrassing for many web site owners.

        The first step is to remain calm.
        
        The second step is to rest assured one of our maintainers will
        address your issue as soon as possible.

        Please make sure you have provided as much information and details
        as possible to help speed up the processing of your whitelisting
        application.

  - type: textarea
    id: record
    attributes:
      label: Domain/URL/IP(s) you believe NOT to be Phishing
      description: |
        Please give us a list of FQDN (domains) or complete links (URL's)
        that you believe are a false positive.
        
        Please warn with "NSFW" where applicable.
      placeholder: |
        example.com
        https://example.org/phishing
        192.0.2.0/24
      render: css
    validations:
      required: true

  - type: checkboxes
    id: source
    attributes:
      label: More Information
      description: |
        How did you discover your IP-address or domain was listed in the
        Phishing or Phishing.Database?
      options:
        - label: mitchellkrogza Phishing
          required: false
        - label: mitchellkrogza Phishing.Database
          required: false
        - label: Website was hacked
          required: false
        - label: Listed as Phishing on Phishtank or OpenPhish
          required: false
        - label: Listed on VirusTotal
          required: false
        - label: Other (Please tell us where in *Related external source* below)
          required: false

  - type: textarea
    id: source_external
    attributes:
      label: Related external source
      description: |
        Please let us know where you found this if not listed above.
        (One link per line.)
      placeholder: |
        https://example.org
      render:
        - markdown
    validations:
      required: false

  - type: textarea
    attributes:
      label: Screenshot
      id: Screenshot
      description: |
        If you feel a screenshot can say more than 1000 hard drives, do
        please feel free to add it here :smiley:

        **INFO** There need to be at least one blank line separating
        before and after the image line

        Copy and paste the lines to the text area below.

        ```
        <details><summary>Click to expand</summary>
        
        
        </details>
        ```
      render: false
    validations:
      required: false

  - type: textarea
    id: description
    attributes:
      label: Describe the issue
      description: |
        Be as clear as possible: nobody can read your mind, and nobody
        is looking over your shoulder.
    validations:
      required: true

  - type: markdown
    attributes:
      value: "## Send a Pull Request for faster removal"
  - type: markdown
    attributes:
      value: |
        Users who understand github and creating Pull Requests can assist
        us with faster removals by sending a PR on the `falsepositive.list`
        file at
        https://github.com/mitchellkrogza/phishing/blob/main/falsepositive.list

        Please include the same above information to help speed up the
        whitelisting process.

# Thanks to @spirillen for taking hes time to make this issue template
# Copyright @spirillen
# - https://mypdns.org/spirillen
# - https://archive.mypdns.org/p/Spirillen/
# - https://github.com/spirillen
# - https://bitbucket.org/spirillen
#
# License: MODIFIED GNU AGPLv3 FOR NON COMMERCIAL USE
# License in full text: https://mypdns.org/mypdns/support/-/wikis/License
#
# Disclaimer:
#   This template can be free of change be used by any NOT for profit and
#   non-profit projects, as long as you keep the links to spirillen in
#   place.
#
# Buy me a coffee: https://ko-fi.com/spirillen
