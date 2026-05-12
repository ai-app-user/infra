#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Configure GitHub CLI authentication for github.com without storing tokens in the repo.

Usage:
  GITHUB_TOKEN=... scripts/gh-auth-token.sh [--hostname github.com]
  scripts/gh-auth-token.sh --token-stdin

Options:
  --hostname HOST   GitHub host to authenticate against. Default: github.com
  --token-stdin     Read token from stdin instead of GITHUB_TOKEN.
  -h, --help        Show this help.

Notes:
  - The token is passed to `gh auth login --with-token`.
  - The script sets git protocol to HTTPS for the selected host.
  - Token scopes for private repos should include `repo`.
USAGE
}

hostname="github.com"
token_stdin=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --hostname)
      hostname="${2:?missing value for --hostname}"
      shift 2
      ;;
    --token-stdin)
      token_stdin=1
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

if ! command -v gh >/dev/null 2>&1; then
  echo "gh is not installed or not on PATH" >&2
  exit 1
fi

if [[ "$token_stdin" -eq 1 ]]; then
  gh auth login --hostname "$hostname" --with-token
else
  if [[ -z "${GITHUB_TOKEN:-}" ]]; then
    echo "GITHUB_TOKEN is not set. Re-run with GITHUB_TOKEN=... or --token-stdin." >&2
    exit 1
  fi
  printf '%s\n' "$GITHUB_TOKEN" | gh auth login --hostname "$hostname" --with-token
fi

gh config set git_protocol https --host "$hostname"
gh auth status --hostname "$hostname"

