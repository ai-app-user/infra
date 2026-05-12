# GitHub Setup

There are three independent pieces of configuration:

1. Server authentication: handled by `gh auth login` or `gh auth login --with-token`.
2. Project destination: the Git remote URL, usually `https://github.com/OWNER/REPO.git`.
3. Commit identity: Git `user.name` and `user.email`.

## Configure a New Server

Interactive:

```bash
gh auth login
gh config set git_protocol https --host github.com
gh auth status
```

Token-based:

```bash
export GITHUB_TOKEN=...
scripts/gh-auth-token.sh
```

The token should not be written into the project. For private repos, the token
needs the `repo` scope.

## Configure a Project Destination

```bash
git remote add origin https://github.com/OWNER/REPO.git
```

Change an existing remote:

```bash
git remote set-url origin https://github.com/OWNER/REPO.git
```

Verify:

```bash
git remote -v
```

## Configure Commit Identity

Global default:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Per-project override:

```bash
git config user.name "Your Name"
git config user.email "you@example.com"
```

