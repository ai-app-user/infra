#!/usr/bin/env bash
# Read-only administrative smoke test. This file is executed with sudo.
set -euo pipefail
printf 'User: '; id -un
printf 'Hostname: '; hostname
printf 'Kernel: '; uname -r
printf 'Uptime: '; uptime -p
printf 'Disk space:\n'; df -h / 
printf 'Memory:\n'; free -h
printf 'Docker availability: '
if command -v docker >/dev/null 2>&1; then docker --version; else echo 'not installed'; fi
