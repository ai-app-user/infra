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

