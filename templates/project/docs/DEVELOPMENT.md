# Development workflow

These instructions apply to all work in this project. For current shared policy,
read [infra](https://github.com/ai-app-user/infra) at the commit in
`.project-bootstrap.json`. This guide explains **how to use** that policy; it
does not replace the authoritative shared standards.

## Before coding

1. Read `AGENTS.md`, `README.md`, this guide, and relevant requirements/designs.
2. Inspect the current code and tests instead of assuming how they work.
3. State the objective, constraints, acceptance criteria, and risks for
   nontrivial work. Ask about essential unknowns instead of inventing decisions.
4. Prefer the smallest coherent change, compatible with the existing architecture.
5. For significant architecture or user-visible behavior changes, document the
   decision and tradeoffs in `docs/` before or alongside implementation.

## Implementation and review

- Follow language/framework conventions established by the project.
- Keep code simple, readable, observable, and appropriately modular.
- Treat inputs, credentials, paths, and network responses as untrusted.
- Use explicit error handling; do not turn failures into silent success.
- Never hardcode or log tokens, keys, passwords, or private customer data.
- Keep application code and project-only dependencies out of `infra`.
- Use a named Git branch for nontrivial changes. Inspect diffs and staged files,
  and never force-push or overwrite work without explicit authorization.
- Avoid scope creep; discuss unrelated improvements separately.

## Testing and delivery

- Add or update automated tests for new behavior, edge cases, failure modes,
  and regressions when practical.
- Run relevant unit/integration/workflow tests and syntax/format checks.
- Test failure handling and repeated execution for bootstrap and automation.
- Document commands and prerequisites in `README.md`.
- Report what changed, which tests ran, what passed or failed, and any remaining
  uncertainty. Never imply deployment or end-to-end testing without evidence.
- For higher-risk changes, prefer a reviewed PR over a direct default-branch push.
- Update runbooks, diagrams, requirements, and changelogs when behavior changes.

## Shared infrastructure lifecycle

**At session/task start:** Read the pinned standards from infra. Check the latest
infra/main when useful and network access is available. An available update is
not automatically applied.

**While developing:** Spot fixes and practices that would benefit more than this
project. Explain them as proposals. Do not globally change policy without user
approval.

**After explicit approval:** Propose a focused change in `ai-app-user/infra` on
a feature branch, include validation and migration notes, and open a PR. Shared
changes only become authoritative after review and merge.

**When adopting a new infra release:** Use the canonical project-bootstrap
`sync` procedure on a clean branch. Compare pinned versus incoming policy,
preview changes, preserve local content with the three-way merge, resolve
conflicts, test, and submit a PR. Update `.project-bootstrap.json` only through
the tool. A release in infra does **not** automatically rewrite this project.

**If external access is unavailable:** Continue only with verified pinned
instructions already available; state what could not be checked. Do not treat
an API/proxy failure as authentication failure without evidence.

## Project-specific setup (complete after bootstrap)

- Purpose and acceptance criteria: see `README.md`
- Architecture and design decisions: add to `docs/`
- Install/build/run commands: add to `README.md`
- Test commands and CI requirements: add to `README.md`
- Deployment/rollback and on-call runbooks: add when applicable
- Project-specific exceptions: record in `AGENTS.md`
