# Security Policy

## Scope

This repository discusses safety classification for chemical and biological risk. It must not be used to publish operational harmful requests, procedures, or jailbreak details.

## Reporting Sensitive Findings

Do not open a public issue containing:

- operational chemical or biological harm instructions;
- full-text C4 or C5 prompts;
- jailbreak strings that bypass ChemBio safeguards;
- model outputs that provide actionable harmful detail.

Use redacted summaries in public discussion. If private vulnerability reporting is enabled for the repository, use that path for sensitive findings.

## Public Issue Format

Use this structure:

```text
Finding type: classifier false positive | classifier false negative | jailbreak severity | documentation issue
Risk level: C0 | C1 | C2 | C3 | C4 | C5
Public-safe summary:
Expected behavior:
Observed behavior:
Recommended fix:
```

