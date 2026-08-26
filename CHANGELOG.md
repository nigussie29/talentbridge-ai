# Changelog

All notable changes to TalentBridge AI are documented here.

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
