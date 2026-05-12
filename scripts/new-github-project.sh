#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Create or connect a local project to a GitHub repo, then push it.

Usage:
  scripts/new-github-project.sh --repo NAME --source DIR [options]

Required:
  --repo NAME       Repository name.
  --source DIR      Local project directory.

Options:
  --owner OWNER     GitHub user/org. Defaults to authenticated gh user.
  --private         Create private repository. Default.
  --public          Create public repository.
  --description TXT Repository description.
  --branch NAME     Branch to push. Default: main.
  --message MSG     Commit message. Default: Initial commit.
  --no-gpg-sign     Commit without Git signing.
  --no-commit       Do not create a commit; only configure remote/create repo.
  --no-push         Do not push.
  --dry-run         Print what would happen.
  -h, --help        Show this help.

Credentials:
  Run `gh auth login` first, or use scripts/gh-auth-token.sh with GITHUB_TOKEN.
USAGE
}

repo=""
source_dir=""
owner=""
visibility="private"
description=""
branch="main"
message="Initial commit"
commit_changes=1
push_changes=1
dry_run=0
no_gpg_sign=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      repo="${2:?missing value for --repo}"
      shift 2
      ;;
    --source)
      source_dir="${2:?missing value for --source}"
      shift 2
      ;;
    --owner)
      owner="${2:?missing value for --owner}"
      shift 2
      ;;
    --private)
      visibility="private"
      shift
      ;;
    --public)
      visibility="public"
      shift
      ;;
    --description)
      description="${2:?missing value for --description}"
      shift 2
      ;;
    --branch)
      branch="${2:?missing value for --branch}"
      shift 2
      ;;
    --message)
      message="${2:?missing value for --message}"
      shift 2
      ;;
    --no-gpg-sign)
      no_gpg_sign=1
      shift
      ;;
    --no-commit)
      commit_changes=0
      shift
      ;;
    --no-push)
      push_changes=0
      shift
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$repo" || -z "$source_dir" ]]; then
  usage >&2
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh is not installed or not on PATH" >&2
  exit 1
fi

if [[ ! -d "$source_dir" ]]; then
  echo "source directory does not exist: $source_dir" >&2
  exit 1
fi

if [[ -z "$owner" ]]; then
  owner="$(gh api user --jq .login)"
fi

full_name="$owner/$repo"
remote_url="https://github.com/$full_name.git"

run() {
  echo "+ $*"
  if [[ "$dry_run" -eq 0 ]]; then
    "$@"
  fi
}

cd "$source_dir"

if [[ ! -d .git ]]; then
  run git init
fi

if [[ -z "$(git config --get user.name || true)" && -n "$(git config --global --get user.name || true)" ]]; then
  run git config user.name "$(git config --global --get user.name)"
fi

if [[ -z "$(git config --get user.email || true)" && -n "$(git config --global --get user.email || true)" ]]; then
  run git config user.email "$(git config --global --get user.email)"
fi

if gh repo view "$full_name" >/dev/null 2>&1; then
  echo "GitHub repo already exists: $full_name"
else
  create_args=(repo create "$full_name" "--$visibility")
  if [[ -n "$description" ]]; then
    create_args+=(--description "$description")
  fi
  run gh "${create_args[@]}"
fi

if git remote get-url origin >/dev/null 2>&1; then
  run git remote set-url origin "$remote_url"
else
  run git remote add origin "$remote_url"
fi

run git branch -M "$branch"

if [[ "$commit_changes" -eq 1 ]]; then
    run git add -A
    if git diff --cached --quiet; then
      echo "No staged changes to commit."
    else
      commit_cmd=(git commit -m "$message")
      if [[ "$no_gpg_sign" -eq 1 ]]; then
        commit_cmd=(git commit --no-gpg-sign -m "$message")
      fi
      run "${commit_cmd[@]}"
    fi
  fi

if [[ "$push_changes" -eq 1 ]]; then
  run git push -u origin "$branch"
fi

echo "Project is configured for $remote_url"
