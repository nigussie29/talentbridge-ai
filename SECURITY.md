# Security Policy

## Supported Version

The deployed `main` branch is the supported TalentBridge AI version.

## Reporting a Vulnerability

Please do not publish credentials, access tokens, private résumés, personal
information, or exploit details in a public issue.

Use the repository's **Security** tab to submit a private vulnerability report.
Include the affected feature, reproduction steps, expected impact, and any
suggested mitigation. If private vulnerability reporting is unavailable, contact
the repository owner through their GitHub profile without including secrets in
the first message.

## Data Protection Expectations

- Supabase secrets belong only in Streamlit secrets or local environment
  configuration and must never be committed.
- Private records must remain protected by Supabase row-level security.
- Stored résumé files must remain owner-scoped and restricted to supported file
  types and sizes.
- Logs and downloadable summaries must not expose authentication tokens or
  private résumé/job-description text.

Security reports will be reviewed before public disclosure. A fix and release
note will be published when remediation is complete.
