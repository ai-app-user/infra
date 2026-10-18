# Project Infra

Small reusable tooling for bootstrapping GitHub-backed projects.

This repo intentionally does not store credentials. Authentication is handled by
GitHub CLI (`gh`) using either an interactive login or a token supplied at
runtime.

## Quick Start

Check the current GitHub setup:

```bash
scripts/check-github-setup.sh
```

Configure `gh` on a new server using a token:

```bash
export GITHUB_TOKEN=...
scripts/gh-auth-token.sh
```

Create and push a new project:

```bash
scripts/new-github-project.sh \
  --repo my-new-project \
  --source /path/to/project \
  --owner ai-app-user \
  --private
```

## Contents

- `scripts/gh-auth-token.sh`: configure GitHub CLI auth from `GITHUB_TOKEN` or stdin.
- `scripts/check-github-setup.sh`: show Git/GitHub auth and project target state.
- `scripts/new-github-project.sh`: initialize a local repo, create GitHub repo if needed, commit, and push.
- `docs/github-setup.md`: how project destination and credentials are configured.
- `docs/project-guidelines.md`: common cross-project engineering rules.
- `docs/security.md`: credential handling rules.


## Project bootstrap

The canonical Codex skill is [project-bootstrap](skills/project-bootstrap/SKILL.md).
It supports local scaffolding, explicit GitHub publishing, safe adoption and
upgrades, and proposing shared improvements through infra pull requests.

```bash
python3 scripts/project-bootstrap.py create --project /workspace/my-project
# Review the plan, then repeat with --apply.
python3 -m unittest discover -s tests -v
```

See [workflow and synchronization](docs/project-bootstrap.md) and
[Codex Cloud activation](docs/codex-cloud.md). This repo includes a skill-only
plugin and marketplace catalog; their presence does **not** install a skill
account-wide. Cloud installation and cross-device discovery remain unverified.
The explicit-fetch fallback works without relying on global skill discovery,
provided the Cloud task can run a shell and access infra.

Prefer project-bootstrap for new projects. The older new-github-project.sh
remains available for existing automation and stages all source files when
committing; review its source directory carefully before use.

## Full VPS administration

For approved root-level VPS maintenance, use the reviewed, manually triggered
[admin workflow](docs/vps-admin.md) in infra. This is deliberately separate
from ordinary project deployment and requires protected environment secrets.
