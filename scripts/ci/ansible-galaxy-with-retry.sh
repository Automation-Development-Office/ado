#!/bin/sh
# Retry ansible-galaxy collection install (Galaxy 504 / resolver flake under parallel CI).
set -eu

if [ "${1:-}" != "collection" ] || [ "${2:-}" != "install" ]; then
  echo "Usage: $0 collection install [ansible-galaxy collection install args...]" >&2
  exit 2
fi
shift 2

max_attempts=3
attempt=1
while [ "$attempt" -le "$max_attempts" ]; do
  if ansible-galaxy collection install "$@"; then
    exit 0
  fi
  if [ "$attempt" -eq "$max_attempts" ]; then
    echo "ansible-galaxy collection install failed after ${max_attempts} attempts: $*" >&2
    exit 1
  fi
  sleep_seconds=$((attempt * 15))
  echo "ansible-galaxy failed (attempt ${attempt}/${max_attempts}); retrying in ${sleep_seconds}s: $*" >&2
  sleep "$sleep_seconds"
  attempt=$((attempt + 1))
done
