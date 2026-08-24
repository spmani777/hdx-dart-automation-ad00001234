name: Feature Request
description: Propose a new feature for DaRT Automation
title: "[FEATURE] <Brief summary>"
labels: ["enhancement", "HDX"]
body:
  - type: markdown
    attributes:
      value: |
        ### DaRT Automation Feature Request (APM ID: AD00001234 | Track: HDX)
  - type: textarea
    id: problem
    attributes:
      label: Business Problem / Motivation
      description: What banking problem does this feature solve?
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: Describe the technical or business solution.
    validations:
      required: true

