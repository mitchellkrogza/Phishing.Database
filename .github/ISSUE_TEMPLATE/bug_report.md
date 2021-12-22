name: Bug report
title: "[BUG]"
description: Create a report to help us improve
labels: ["bug"]
assignees:
  - mitchellkrogza
  - funilrys
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!

  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Also tell us, what did you expect to happen?
      placeholder: Tell us what you see!
      value: "A bug happened!"
    validations:
      required: true
  
  - type: textarea
    id: expected-behaviour
    attributes:
      label: Expected behaviour?
      description: Also tell us, what did you expect to happen?
      placeholder: Tell us what you see!
      value: "A unexpected thing happened!"
    validations:
      required: false

  - type: textarea
    attributes:
      label: Screenshot
      id: Screenshot
      description: |
        If you feel a screenshot can say more than 1000 hard drives, do
        please feel free to add it here :smiley:

        **INFO** There need to be at least one blank line separating before
        and after the image line

        Copy and paste the lines to the text area below.

        ```
        <details><summary>Click to expand</summary>
        
        
        </details>
        ```
      render: false
    validations:
      required: false

  - type: textarea
    id: additional-context
    attributes:
      label: Additional context
      description: |
        Add any other context about the problem here.
    validations:
      required: false

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
