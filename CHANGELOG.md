# Changelog

All notable changes to TalentBridge AI are documented here.

## Phase 5C — Production Monitoring — 2026-08-26

### Added

- Added an hourly GitHub Actions uptime check for the public application and
  Streamlit health endpoint, with a manual run option.
- Added a visible Production Health Check in the Beta Test Center for the Python
  runtime, application dependencies, and Supabase configuration.
- Added downloadable privacy-safe health reports and allow-listed structured
  monitoring events that exclude résumés, job descriptions, account details,
  and secret values.
- Added automated monitoring tests for healthy, degraded, and privacy behavior.

## Phase 5B — UI and Mobile Polish — 2026-08-26

### Added

- Added responsive single-column stacking for forms, score cards, ratings, and
  other multi-column sections on phone-sized screens.
- Added horizontally scrollable primary tabs and wide result tables so content
  remains reachable on narrow screens.
- Added accessible keyboard focus indicators, larger touch targets, a skip link,
  reduced-motion support, and responsive hero typography.
- Added a visible Mobile & Accessibility Check in the Beta Test Center covering
  mobile layout, tab access, keyboard focus, 200% zoom, tables, and downloads.
- Added automated coverage for the Phase 5B interface checklist.

## Phase 5A — Beta User Testing — 2026-08-26

### Added

- Added an in-app Beta Test Center with role-specific Job Seeker,
  HR / Recruiter, and Training Center scenarios.
- Added scenario completion tracking, 1–5 experience ratings, issue severity,
  privacy-safe notes, and Passed / Needs Review / Blocked session results.
- Added downloadable beta feedback reports that intentionally exclude résumé
  and job-description text and require no new database migration.
- Added automated tests for beta plan coverage, role validation, report status,
  rating normalization, and feedback sanitization.

## MVP — 2026-08

### Added

- Supabase authentication with role-locked Job Seeker, HR / Recruiter, and
  Training Center experiences.
- Private, reusable résumé and job-description storage with owner-scoped access.
- Saved analyses, before/after comparison, progress dashboards, downloadable
  progress reports, and best-version selection.
- Required-versus-preferred skill classification, evidence traceability,
  requirement-evidence strength, and evidence-adjusted scoring.
- Input-quality, confidence, critical-requirement, and application-decision
  guardrails.
- Career-specific readiness, learning plans, portfolio evidence, interview
  preparation, HR batch screening, and downloadable mode reports.
- Best-version application plan for a private-input-safe application workflow.
- Automated GitHub CI for tests, compilation, and dependency validation.

### Security

- Added private-data deletion controls, Supabase row-level security guidance,
  secret-handling guidance, and a vulnerability-reporting policy.

### Notes

TalentBridge results are evidence-based guidance. They do not verify proficiency,
make an employer decision, or guarantee an interview.
