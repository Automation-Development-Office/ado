#!/usr/bin/env bash
# Install Molecule base collections and all scenario requirements.yml once for CI cache.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
collections_path="${ANSIBLE_COLLECTIONS_PATH:-${HOME}/.ansible/collections}"
mkdir -p "$collections_path"
export ANSIBLE_COLLECTIONS_PATH="$collections_path"

galaxy_retry() {
  sh "${repo_root}/scripts/ci/ansible-galaxy-with-retry.sh" collection install "$@"
}

# Local collection without galaxy.yml deps; matrix jobs overlay PR checkout later.
galaxy_retry "${repo_root}" --force --no-deps -p "$collections_path"
galaxy_retry ansible.posix --force -p "$collections_path"
galaxy_retry community.general --force -p "$collections_path"
galaxy_retry containers.podman --force -p "$collections_path"

while IFS= read -r requirements_file; do
  echo "Installing scenario requirements: ${requirements_file}"
  galaxy_retry -r "$requirements_file" -p "$collections_path"
done < <(find "${repo_root}/extensions/molecule" -name requirements.yml | sort)

echo "Molecule collections cache ready under ${collections_path}"
