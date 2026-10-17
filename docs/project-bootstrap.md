# Project bootstrap

The canonical standards are `docs/project-guidelines.md` and `docs/security.md`.
`standards.json` versions these documents and maps managed templates. Projects
store references, project-specific instructions, and `.project-bootstrap.json`.
The state contains the exact infra commit, bundle digest, version, and previous
rendered templates for offline three-way merging. Those template baselines are
merge metadata, not independently maintained copies of shared standards.

## Commands

From a committed infra checkout (Python 3 and Git required):

```bash
python3 scripts/project-bootstrap.py create --project /workspace/example
python3 scripts/project-bootstrap.py create --project /workspace/example --apply
python3 scripts/project-bootstrap.py sync --project /workspace/existing --adopt-existing
python3 scripts/project-bootstrap.py sync --project /workspace/existing --adopt-existing --apply
# Explicit remote mutation, only when requested:
python3 scripts/project-bootstrap.py publish --project /workspace/example --owner ai-app-user --repo example
```

Create and sync are offline. Preview is the default and never creates a directory.
Sync requires an existing directory. `--adopt-existing` preserves existing files
on initial adoption; add the infra reference to an existing AGENTS.md manually
with review so future agents can discover the workflow. No language/framework is
assumed. Add project-specific code, testing, and dependencies as a separate step.

Publish checks API authentication and repository lookup before mutations. Only
an explicit HTTP 404 permits creation; network/permission errors stop it. A 404
can also mean an inaccessible private repository: GitHub must still authorize
creation, and creation failures stop the operation. Existing unrelated remotes,
nested repositories, staged changes, and missing identity are rejected. Only
managed files are staged. Pushes are never forced. Repeating publication uses
the existing repository and does not create an empty commit. Existing remote
history may require a normal fetch/integration; it is never overwritten.

## Safe updates

For upgrades, use a clean named project branch and a reviewed infra commit.
Compare incoming infra documents as well as the generated diff. The updater
checks that the bundle matches the recorded infra commit. It refuses downgrades,
unsafe paths, symlinks in managed paths, malformed state, and overlapping edits.

Unchanged upstream files preserve project customizations. Nonoverlapping edits
merge through `git merge-file`. An unchanged locally deleted file stays deleted;
an upstream change to that file conflicts. Removed upstream files are deleted
only if locally unchanged. Every conflict aborts the complete plan before writes.
Resolve conflicts by reconciling the local file with the incoming template, then
rerun; the original state remains the merge base until success. Do not delete it.
Writes use per-file atomic replacement with state last, not a filesystem-wide
transaction. Reruns after interruption are safe for already applied incoming
content. Do not run concurrent syncs or edit managed files during sync.

Version policy: bump patch for compatible clarifications, minor for additive
standards, major for breaking changes requiring project-specific migration.
Breaking semantic migrations require explicit review; text merging cannot prove
application compatibility. Run project tests and submit an upgrade PR. No
background auto-updates or mass synchronization is performed.

## Improving the system

A project's AGENTS.md instructs Codex to recognize and propose reusable changes.
This is guidance, not an autonomous background monitor. The canonical skill
turns an explicit global-improvement request into an infra PR. Nothing changes
globally until that PR is reviewed and merged; projects adopt it separately.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Tests use temporary local Git repositories and fake GitHub CLI responses. Real
Git performs initialization, staging, committing, merging, and pushes to local
bare repositories. No tests create GitHub repositories or need credentials.
Remote API authorization and Cloud plugin discovery require separate live
verification and must not be inferred from these tests.
