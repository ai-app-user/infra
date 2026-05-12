#!/usr/bin/env bash
set -euo pipefail

hostname="${1:-github.com}"

echo "== gh auth =="
if command -v gh >/dev/null 2>&1; then
  gh auth status --hostname "$hostname" || true
  echo
  echo "== gh user =="
  gh api --hostname "$hostname" user --jq '{login: .login, name: .name, email: .email}' 2>/dev/null || true
else
  echo "gh is not installed or not on PATH"
fi

echo
echo "== git identity =="
echo "global user.name:  $(git config --global --get user.name || true)"
echo "global user.email: $(git config --global --get user.email || true)"
echo "local user.name:   $(git config --get user.name || true)"
echo "local user.email:  $(git config --get user.email || true)"

echo
echo "== git remote =="
git remote -v 2>/dev/null || true

echo
echo "== ssh public key fingerprints =="
for key in "$HOME"/.ssh/*.pub; do
  [[ -e "$key" ]] || continue
  echo "$key"
  ssh-keygen -lf "$key" || true
done

