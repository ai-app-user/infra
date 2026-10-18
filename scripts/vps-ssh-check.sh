#!/usr/bin/env bash
# Read-only connectivity probe. No password fallback or insecure host-key flags.
set -euo pipefail
: "${VPS_HOST:?Set VPS_HOST to an approved host}"
: "${VPS_USER:?Set VPS_USER to an approved non-root SSH user}"
port="${VPS_PORT:-22}"
if [[ ! "$port" =~ ^[0-9]+$ ]] || (( 10#$port < 1 || 10#$port > 65535 )); then
  echo "Invalid VPS_PORT" >&2; exit 2
fi
args=(-o BatchMode=yes -o NumberOfPasswordPrompts=0
      -o StrictHostKeyChecking=yes -o ConnectTimeout=10
      -o IdentitiesOnly=yes -p "$port")
if [[ -n "${VPS_IDENTITY_FILE:-}" ]]; then
  [[ -f "$VPS_IDENTITY_FILE" ]] || { echo "Identity file not found" >&2; exit 2; }
  args+=(-i "$VPS_IDENTITY_FILE")
fi
# Restrict the arguments to environment variables; do not print credentials.
ssh "${args[@]}" -- "${VPS_USER}@${VPS_HOST}" 'id -un'
