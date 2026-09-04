#!/usr/bin/env bash
# Install native build deps before tox ade install (systemd-python, etc.).
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${repo_root}"

declare -A package_set=()

add_packages() {
  local pkg
  for pkg in "$@"; do
    [[ -n "${pkg}" ]] || continue
    package_set["${pkg}"]=1
  done
}

install_packages() {
  local packages=("$@")
  if [[ "${#packages[@]}" -eq 0 ]]; then
    return 0
  fi
  if command -v apt-get >/dev/null 2>&1; then
    if command -v sudo >/dev/null 2>&1 && [[ "$(id -u)" -ne 0 ]]; then
      sudo apt-get update -qq
      sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${packages[@]}"
    else
      apt-get update -qq
      DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${packages[@]}"
    fi
    return 0
  fi
  if command -v dnf >/dev/null 2>&1; then
    if command -v sudo >/dev/null 2>&1 && [[ "$(id -u)" -ne 0 ]]; then
      sudo dnf install -y "${packages[@]}"
    else
      dnf install -y "${packages[@]}"
    fi
    return 0
  fi
  echo "WARN: No supported package manager; skipping system dependency install." >&2
  return 1
}

bindep_cmd=""
if [[ -n "${TOX_ENV_DIR:-}" && -x "${TOX_ENV_DIR}/bin/bindep" ]]; then
  bindep_cmd="${TOX_ENV_DIR}/bin/bindep"
elif command -v bindep >/dev/null 2>&1; then
  bindep_cmd="bindep"
fi

if [[ -f bindep.txt && -n "${bindep_cmd}" ]]; then
  while IFS= read -r pkg; do
    add_packages "${pkg}"
  done < <("${bindep_cmd}" -b -f bindep.txt -l newline 2>/dev/null || true)
fi

if command -v apt-get >/dev/null 2>&1; then
  add_packages libsystemd-dev libsystemd0 pkg-config gcc build-essential
elif command -v dnf >/dev/null 2>&1; then
  add_packages systemd-devel pkg-config gcc
fi

if [[ "${#package_set[@]}" -eq 0 ]]; then
  echo "WARN: No system packages selected for install." >&2
  exit 0
fi

mapfile -t packages < <(printf '%s\n' "${!package_set[@]}" | sort)
echo "Installing system packages for tox ade install: ${packages[*]}"
install_packages "${packages[@]}"

if command -v pkg-config >/dev/null 2>&1; then
  if ! pkg-config --exists libsystemd libsystemd-journal 2>/dev/null; then
    echo "ERROR: libsystemd is still missing after package install (needed for systemd-python)." >&2
    pkg-config --list-all 2>/dev/null | grep -i systemd || true
    exit 1
  fi
  echo "OK: pkg-config found libsystemd."
fi
