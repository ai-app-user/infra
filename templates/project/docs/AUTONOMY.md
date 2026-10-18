# Autonomous project delivery contract

**Default when the user asks Codex to build or change something:** Complete the
requested task rather than stopping after drafting documents, opening a PR,
or listing steps for the user. Work through the available tools until a usable
and verified outcome is achieved, or until a concrete blocker is found.

## Meaning of "done"

- **Documentation task:** the files are committed, validated, and merged into
  the project default branch when checks and applicable rules allow.
- **Implementation task:** working code and tests are committed, validated and
  merged; documentation reflects the delivered behavior.
- **Deployment task:** the approved target has actually been deployed, health
  checked, and the access URL or result reported. A merge alone is not a deploy.
- **Planning-only request:** stop at the specifically requested plan or preview;
  never create repositories, merge, or deploy against an explicit preview-only
  instruction.

## Working loop

1. Read AGENTS.md, the pinned infra policies, product requirements and relevant
   code before implementing. Do not substitute a plan for the user's actual task.
2. Write acceptance criteria and implement in focused steps; tests, validation,
   documentation and configuration are part of the change.
3. Run appropriate automated checks and examine failures. Fix routine failures
   and rerun; do not claim success with red or missing required checks.
4. Create a named feature branch and PR when appropriate. For ordinary changes
   in a user-owned project, **merge the PR automatically** using approved GitHub
   capabilities after tests and checks pass, no conflicts exist, and the diff
   matches the authorized scope. Do not ask the user to click the merge button.
   If GitHub API is unavailable to Codex Cloud, use a connected GitHub integration
   or configured GitHub auto-merge. Never bypass required branch protection.
5. Where the user authorized deployment, continue to deployment using the
   project's documented steps and supported automation, then verify service
   health. Prefer reversible changes and isolate apps on shared hosts.
6. Report the actual result: commits/PR merge status, tests run, deployment
   address, health checks, and anything blocked.

## Safety and stop conditions

Ask before proceeding when a key product/security decision is missing, the
operation is outside the authorized scope, credentials are unavailable, tests
are failing without a safe fix, merge conflicts cannot be resolved without
overwriting work, or deployment could irreversibly destroy data, access,
security boundaries or affect unrelated workloads.

Never interpret "full access" as approval to expose credentials or turn off
protections. For VPS tasks, use the private vps-control integration only for
user-authorized changes; avoid root when a project-scoped deploy identity works.
Maintain rollback paths, backups when needed, and actual health checks.

Never auto-merge untrusted external contributions, shared infra global policy
changes, dependency major/security-sensitive upgrades, or modifications to
privileged deployment/control-plane workflows without explicit authorization.
The **infra** repository's own shared standards continue to require reviewed
changes unless the user specifically authorizes the particular update.

## Across Codex sessions

AGENTS.md supplies instructions when Codex works inside the repository, but
**does not start background work, schedule future tasks, or guarantee that a
terminated Codex task continues working**. A task must be active or an explicit
Codex/GitHub automation configured for continued operations. Report such limits
instead of promising invisible ongoing work.

The GitHub Actions VPS gateway executes a submitted authorized job automatically;
it does not itself implement the application. Likewise automatic PR merging is
conditional on passing checks, not a substitute for tests.

## New project first session

The first real development request is the start of work. Load the applicable
instructions and inspect the repository as part of that request. Do not ask
for a separate readiness conversation or stand-alone bootstrap verification
unless a real access/configuration failure blocks work.
