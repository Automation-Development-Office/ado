#!/usr/bin/env bash
# Install native build deps before tox ade install (systemd-python, etc.).
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${repo_root}"

install_packages() {
  if [[ "$#" -eq 0 ]]; then
    return 0
  fi
  if command -v apt-get >/dev/null 2>&1; then
    if command -v sudo >/dev/null 2>&1 && [[ "$(id -u)" -ne 0 ]]; then
      sudo apt-get update -qq
      sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "$@"
    else
      apt-get update -qq
      DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "$@"
    fi
    return 0
  fi
  if command -v dnf >/dev/null 2>&1; then
    if command -v sudo >/dev/null 2>&1 && [[ "$(id -u)" -ne 0 ]]; then
      sudo dnf install -y "$@"
    else
      dnf install -y "$@"
    fi
    return 0
  fi
  echo "WARN: No supported package manager; skipping system dependency install." >&2
}

bindep_cmd=""
if [[ -n "${TOX_ENV_DIR:-}" && -x "${TOX_ENV_DIR}/bin/bindep" ]]; then
  bindep_cmd="${TOX_ENV_DIR}/bin/bindep"
elif command -v bindep >/dev/null 2>&1; then
  bindep_cmd="bindep"
fi

if [[ -f bindep.txt && -n "${bindep_cmd}" ]]; then
  mapfile -t packages < <("${bindep_cmd}" -b -f bindep.txt -l newline)
  if [[ ${#packages[@]} -gt 0 ]]; then
    install_packages "${packages[@]}"
    exit 0
  fi
fi

if command -v apt-get >/dev/null 2>&1; then
  install_packages libsystemd-dev pkg-config gcc build-essential
elif command -v dnf >/dev/null 2>&1; then
  install_packages systemd-devel pkg-config gcc
fi
