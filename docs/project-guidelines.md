# Common Project Guidelines

## Repository layout

Prefer predictable organization appropriate to project size:

```text
README.md
AGENTS.md
.project-bootstrap.json
docs/DEVELOPMENT.md
docs/
scripts/
src/
tests/
config/
```

Do not create empty directories merely for appearances. Keep generated build
artifacts, datasets, logs, sensitive material, and secrets out of Git.

## Working agreement

- Understand the user-visible objective, constraints, and acceptance criteria.
  Distinguish requirements from assumptions.
- For material changes, summarize the plan and risks before implementation.
  Prefer small, reviewable, reversible changes to speculative rewrites.
- Preserve established conventions and project-specific requirements.
- Keep reusable infrastructure separate from application-specific code.
- Prefer short, repeatable tooling under `scripts/` when needed.
- Keep requirements, architecture decisions, runbooks, and performance notes
  near the code they govern. Update documentation when behavior changes.
- Report accurately what has been tested, deployed, or left unverified.

## Testing and quality

Select applicable levels rather than inventing a universal test command:
- Unit tests for isolated behavior and edge cases.
- Integration tests for component boundaries, real failure handling, and retries.
- Functional or end-to-end tests for supported user workflows.
- Performance and reliability tests when these are part of acceptance criteria.

Review the diff, run relevant checks, and investigate failures. Do not declare
success merely because a command returned or the code was committed.

## Security and credentials

Read `docs/security.md` from the same pinned infra commit. Validate inputs,
minimize permissions, protect secrets, and do not execute unknown contributions
as privileged trusted instructions. Never commit credentials, private keys,
customer data, or generated sensitive artifacts.

## Git and review hygiene

- Inspect `git status --short` and diffs before staging.
- Keep commits focused, with meaningful descriptions.
- Use branches and reviewed PRs for nontrivial or risky work.
- Avoid destructive Git operations and direct default-branch changes unless
  explicitly approved.
- Check automation idempotency and conflict behavior before publishing.

## Relationship to shared infrastructure

At the start of a coding session, use the project's `AGENTS.md` and pinned
infra version as the baseline. Periodically compare against trusted infra/main
when working on a relevant change, but never auto-adopt unreviewed changes.

Reusable lessons should become **proposals** to infra, including impact,
compatibility, validation, and a reviewable PR after user approval.
Existing projects update through the version-aware bootstrap sync workflow.
There is no guarantee of autonomous background checks or global skill discovery.
