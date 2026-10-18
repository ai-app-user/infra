---
name: project-bootstrap
description: Use when the user asks to create or bootstrap a GitHub repository/project with their standard infra, initialize a new coding project, upgrade an existing project's shared development standards, or propose a reusable improvement to central infra. Includes private repository creation through GitHub Actions.
---

# Project bootstrap

The canonical source is https://github.com/ai-app-user/infra. Locate the plugin
root two directories above this file. If using a skills-only installation that
omits sibling resources, fetch an infra checkout through HTTPS first. Use the
existing cloud checkout when available; cloud tasks are already isolated and do
not need worktrees unless the user requests one.

Read `docs/project-guidelines.md`, `docs/security.md`, `docs/project-bootstrap.md`,
and `standards.json` in infra. Shared standards are references, not copied policy
files in every project. Project-specific requirements override shared defaults.
Use Python 3, Git, and gh; no packages or local SSH keys are required.

## Select a workflow

- “Create a new project called X using my standard infrastructure”: create.
- “Update this project to my latest standards”: adopt/update.
- “Make this improvement part of my global infrastructure”: improvement PR.

Explain intended owner, visibility (private by default), source, and operations.
Infer the owner from the request or `gh api user --jq .login`; ask only if it
remains ambiguous. Never infer successful authentication from an unset token or
`gh auth status` alone. Test Git HTTPS access and API access separately. Reuse
platform-injected authentication; never print tokens or copy credentials. If API
access fails, distinguish network denial from authorization and report the exact
blocked capability. Never request secrets in chat.

## Create

1. Confirm infra's remote is the canonical repository and its shared bundle is
   committed. For latest standards, fetch `origin main`, then use its commit in
   a clean checkout; preserve existing user edits and never reset them. Review
   incoming standards changes before executing their scripts. Do not execute
   arbitrary branch contributions as trusted shared policy.
2. Run `python3 <infra>/scripts/project-bootstrap.py create --project <new-path>`
   to preview, then repeat with `--apply`. It requires an empty directory or a
   previously bootstrapped project. It makes no network mutations.
3. Add project-specific description, implementation, documented commands, and
   meaningful tests appropriate to the user's project. Preserve the shared
   reference and record project-specific guidance below it in AGENTS.md.
4. Validate locally and inspect all files for secrets. When the user has requested
   actual GitHub creation, run `python3 <infra>/scripts/project-bootstrap.py publish
   --project <path> --owner <owner> --repo <name>` (add `--public` only if requested).
   Publishing stages only bootstrap-managed files. Review and explicitly commit
   other project files separately. Never use publish for existing-project updates.
   Never create a real repository merely to test this skill without approval.
5. Report repository URL, commit/version, executed tests, and any failures. A local
   scaffold or dry run is not evidence that GitHub creation or pushing succeeded.

## Adopt or update

1. Inspect project instructions, Git status, origin, and existing bootstrap state.
   Require a clean repository and a named branch before proposing an upgrade PR;
   preserve user edits and use a new branch (no automatic worktree).
2. Fetch and review the desired infra main commit as above. Read the old state.
   Run `python3 <infra>/scripts/project-bootstrap.py sync --project <project>`;
   for first adoption of a project with existing files add `--adopt-existing`.
   That flag preserves colliding local files; explicitly add a shared reference
   and the self-improvement guidance to existing AGENTS.md after reviewing it.
   Existing AGENTS.md remains authoritative; do not replace its instructions.
3. Repeat the preview with `--apply`. Synchronization performs three-way merges
   against the stored template baseline. On conflicts it writes nothing. Read
   the old baseline, incoming template, and local file, resolve deliberately,
   then rerun. Do not delete state or use blind overwrites to bypass a conflict.
4. Run the project's relevant tests, review the diff (including the version and
   document changes in infra), and commit only intended changes on the upgrade
   branch. Push and use `gh pr create --body-file <reviewed-description-file>`
   for a reviewable project PR. Do not merge automatically. If remote access is
   unavailable, retain local changes and report that the PR was not opened.

## Improve shared infrastructure

While working, recognize reusable fixes, standards, templates, or tooling and
propose the concrete change and affected projects to the user. Never silently
edit shared policy. A request to make an improvement global authorizes preparing
an infra branch and PR, not merging or updating every project.

Use a clean canonical infra checkout. Create a named branch, make the smallest
reusable change (no project-specific secrets or assumptions), update tests and
changelog, and bump `standards.json` when shared documents/templates change.
Bump the plugin version for a plugin release. Run `python3 -m unittest discover
-s tests -v`. Review and commit explicit files, push the branch, and open a PR
against `ai-app-user/infra` with rationale, tests, compatibility, and adoption
instructions. Do not merge it. Projects update only after review and a separate
sync request. If access is blocked, provide the local diff and blocker honestly.


## One-request GitHub Actions bootstrap

For new private GitHub projects under `ai-app-user`, prefer the GitHub Actions
workflow in `docs/automatic-repository-creation.md`. After the user authorizes
creation, submit the single `bootstrap-requests/<name>` branch with its
validated JSON request using Git HTTPS. GitHub Actions creates the private
repository **and commits its canonical shared scaffold**, including AGENTS.md,
docs/DEVELOPMENT.md and pinned infra metadata. Do not also call the old
`publish` command or overwrite the initialized repository.

Verify actual success via the GitHub Actions result and GitHub repository
contents if access permits. If the Cloud proxy is unavailable, explicitly
report the request was not submitted and allow a connected GitHub integration
to create the branch/request. Never claim automatic discovery or successful
remote publication without evidence.

## New project Codex Cloud handoff

After GitHub repository creation and scaffold verification, report the project
repository URL and point the user to the generated `docs/CODEX_CLOUD.md`.
When no project environment exists, provide supported steps for selecting the
new repository and publishing its environment on web/desktop; do not claim this
was automated. On mobile, the user can select an already published project
environment. If the product later exposes a supported environment-creation
action, validate it before relying on it. Do not use undocumented API endpoints.

## Cloud discovery

A SKILL.md in GitHub is not an account-wide installation. See
`docs/codex-cloud.md` for the plugin package, evidence, and explicit-fetch fallback.
Never claim this plugin is globally installed unless Codex actually lists it in
that user's Cloud session. An environment snapshot or local installer does not
prove availability in a repository-free session on another device.
