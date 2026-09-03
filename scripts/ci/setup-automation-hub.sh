#!/usr/bin/env bash
# Normalize Automation Hub env vars and optional token file for local and CI use.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${repo_root}"

token="${ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN:-${AUTOMATION_HUB_TOKEN:-}}"

export ANSIBLE_GALAXY_SERVER_LIST="${ANSIBLE_GALAXY_SERVER_LIST:-certified,galaxy}"
export ANSIBLE_GALAXY_SERVER_GALAXY_URL="${ANSIBLE_GALAXY_SERVER_GALAXY_URL:-https://galaxy.ansible.com/}"
export ANSIBLE_GALAXY_SERVER_CERTIFIED_URL="${ANSIBLE_GALAXY_SERVER_CERTIFIED_URL:-https://console.redhat.com/api/automation-hub/content/published/}"
export ANSIBLE_GALAXY_SERVER_CERTIFIED_AUTH_URL="${ANSIBLE_GALAXY_SERVER_CERTIFIED_AUTH_URL:-https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token}"
export ANSIBLE_GALAXY_SERVER_TIMEOUT="${ANSIBLE_GALAXY_SERVER_TIMEOUT:-120}"

if [[ -n "${token}" ]]; then
  export ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN="${token}"
  export AUTOMATION_HUB_TOKEN="${token}"
  mkdir -p .ansible
  printf '%s' "${token}" > .ansible/automation_hub_token
  chmod 600 .ansible/automation_hub_token
fi
