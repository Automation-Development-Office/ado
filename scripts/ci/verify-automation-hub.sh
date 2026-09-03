#!/usr/bin/env bash
# Verify console.redhat.com Automation Hub URLs and optional token auth.
set -euo pipefail

# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")/setup-automation-hub.sh"

HUB_PUBLISHED_URL="${AUTOMATION_HUB_PUBLISHED_URL:-${ANSIBLE_GALAXY_SERVER_CERTIFIED_URL}}"
HUB_AUTH_URL="${AUTOMATION_HUB_AUTH_URL:-${ANSIBLE_GALAXY_SERVER_CERTIFIED_AUTH_URL}}"
GALAXY_URL="${ANSIBLE_GALAXY_SERVER_GALAXY_URL}"
GALAXY_URL="${GALAXY_URL%/}"
TOKEN="${ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN:-}"

probe_url() {
  local label="$1"
  local url="$2"
  local expected="${3:-401}"
  local code
  code="$(curl -s -o /dev/null -w '%{http_code}' -L "$url" || true)"
  if [[ "$code" != "$expected" ]]; then
    echo "ERROR: ${label} returned HTTP ${code}; expected ${expected}."
    echo "  URL: ${url}"
    exit 1
  fi
  echo "OK: ${label} reachable (HTTP ${code} without auth)."
}

probe_url "Automation Hub published API" "${HUB_PUBLISHED_URL}"
probe_url "Ansible Galaxy API" "${GALAXY_URL}/api/" "200"

if [[ -z "${TOKEN}" ]]; then
  echo "WARN: No Automation Hub token in environment; skipping authenticated install check."
  exit 0
fi

tmpdir="$(mktemp -d)"
trap 'rm -rf "${tmpdir}"' EXIT

export ANSIBLE_COLLECTIONS_PATH="${tmpdir}"

echo "Checking authenticated install of ansible.platform from Automation Hub..."
ansible-galaxy collection install ansible.platform -p "${tmpdir}" --force >/dev/null

if [[ ! -d "${tmpdir}/ansible_collections/ansible/platform" ]]; then
  echo "ERROR: ansible.platform was not installed to the expected collections path."
  exit 1
fi

echo "OK: AUTOMATION_HUB_TOKEN can install certified collections from console.redhat.com."
