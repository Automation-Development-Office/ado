#!/usr/bin/env bash
# Verify console.redhat.com Automation Hub URLs and optional token auth.
set -euo pipefail

# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")/setup-automation-hub.sh"

HUB_PUBLISHED_URL="${AUTOMATION_HUB_PUBLISHED_URL:-${ANSIBLE_GALAXY_SERVER_CERTIFIED_URL}}"
GALAXY_URL="${ANSIBLE_GALAXY_SERVER_GALAXY_URL}"
GALAXY_URL="${GALAXY_URL%/}"
TOKEN="${ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN:-}"

probe_url() {
  local label="$1"
  local url="$2"
  shift 2
  local expected_codes=("$@")
  if [[ "${#expected_codes[@]}" -eq 0 ]]; then
    expected_codes=(401)
  fi
  local code
  local allowed
  code="$(curl -s -o /dev/null -w '%{http_code}' -L "$url" || true)"
  for allowed in "${expected_codes[@]}"; do
    if [[ "$code" == "$allowed" ]]; then
      echo "OK: ${label} reachable (HTTP ${code} without auth)."
      return 0
    fi
  done
  echo "ERROR: ${label} returned HTTP ${code}; expected one of: ${expected_codes[*]}." >&2
  echo "  URL: ${url}" >&2
  exit 1
}

# Hub published API requires credentials; 401 is the usual response without a token.
# Accept 403 as well: some gateways/proxies report missing auth as Forbidden rather
# than Unauthorized. Either code means the endpoint is up and not anonymously open.
# Galaxy stays strict at 200; token + ansible.platform install is the real Hub auth test.
probe_url "Automation Hub published API" "${HUB_PUBLISHED_URL}" 401 403
probe_url "Ansible Galaxy API" "${GALAXY_URL}/api/" 200

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
