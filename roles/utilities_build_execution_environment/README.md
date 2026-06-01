# Role: ado.utilities_build_execution_environment

Build a custom Ansible **Execution Environment (EE)** image with `ansible-builder`.

- Uses a caller-provided base EE image
- Pulls the base image from a caller-provided source repository
- Adds caller-provided Galaxy collections and/or local collection artifacts during the EE build

---

## Requirements

- Ansible >= 2.14
- `ansible-builder` available on the managed host where the role runs
- Container runtime dependencies required by `ansible-builder`

---

## Variables

| Variable | Description |
|---------|-------------|
| `utilities_build_execution_environment_base_ee` | Base EE image name and tag (for example `ee-minimal-rhel9:latest`). **Required.** |
| `utilities_build_execution_environment_source_image_repository` | Source image repository path used with the base EE image name (for example `registry.redhat.io/ansible-automation-platform-24`). **Required.** |
| `utilities_build_execution_environment_collections` | List of Ansible collections to include in the EE image. Default: `[]`. |
| `utilities_build_execution_environment_collection_files` | List of local built collection artifact files (`*.tar.gz`). The role copies them into build context and installs them with `type: file`. Default: `[]`. |
| `utilities_build_execution_environment_output_image` | Output image name and tag for the built EE. Default: `custom-ee:latest`. |
| `utilities_build_execution_environment_build_context` | Build context directory used by `ansible-builder`. Default: `/tmp/utilities_build_execution_environment`. |
| `utilities_build_execution_environment_builder_executable` | `ansible-builder` executable name or full path. Default: `ansible-builder`. |
| `utilities_build_execution_environment_package_manager_path` | Package manager path inside the base image used by `ansible-builder` (for example `/usr/bin/microdnf` or `/usr/bin/dnf`). Default: `/usr/bin/microdnf`. |

### Auth via environment (optional)

No role-specific environment authentication variables are required by this role.

At least one of `utilities_build_execution_environment_collections` or
`utilities_build_execution_environment_collection_files` must be non-empty.

---

## Examples

### Build a custom EE image
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.utilities_build_execution_environment
      vars:
        utilities_build_execution_environment_base_ee: ee-minimal-rhel9:latest
        utilities_build_execution_environment_source_image_repository: registry.redhat.io/ansible-automation-platform-24
        utilities_build_execution_environment_collections:
          - ansible.posix
          - community.general
        utilities_build_execution_environment_output_image: localhost/custom-ee:latest
```

### Build with a custom context directory
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.utilities_build_execution_environment
      vars:
        utilities_build_execution_environment_base_ee: ee-supported-rhel9:latest
        utilities_build_execution_environment_source_image_repository: quay.io/ansible
        utilities_build_execution_environment_collections:
          - community.general
        utilities_build_execution_environment_build_context: /tmp/ee-build-demo
        utilities_build_execution_environment_output_image: localhost/custom-ee:demo
```

### Build using a local collection artifact
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.utilities_build_execution_environment
      vars:
        utilities_build_execution_environment_base_ee: ee-minimal-rhel9:latest
        utilities_build_execution_environment_source_image_repository: registry.redhat.io/ansible-automation-platform-24
        utilities_build_execution_environment_collections:
          - ansible.posix
        utilities_build_execution_environment_collection_files:
          - /tmp/builds/infra-ado-0.1.0.tar.gz
        utilities_build_execution_environment_output_image: localhost/custom-ee:with-local
```

---

## Behavior Notes

- The role composes the base image reference from repository + base EE image.
- It renders `execution-environment.yml` and `requirements.yml` into the build context.
- It runs `ansible-builder build` using the rendered files and selected output tag.
- It validates local artifact paths from `utilities_build_execution_environment_collection_files` before build.
- It injects local collection artifacts via `additional_build_files` into `collection-artifacts/` inside `_build`.
- It sets `options.package_manager_path` in the EE definition to match the selected base image.
- Required inputs are enforced by role argument specs and runtime assertions.

---

## Molecule

Use the extension integration scenario at
`extensions/molecule/integration_utilities_build_execution_environment`.

Install collection and dependencies before running locally:

```bash
cd /path/to/your/git/checkout/infra.ado
ansible-galaxy collection install . --force -p ~/.ansible/collections
ansible-galaxy collection install ansible.posix --force -p ~/.ansible/collections
ansible-galaxy collection install community.general --force -p ~/.ansible/collections
export ANSIBLE_COLLECTIONS_PATH="$HOME/.ansible/collections:/usr/share/ansible/collections"
```

Run integration scenario locally:

```bash
cd extensions
molecule test -s integration_utilities_build_execution_environment
```

If your environment restricts writes under `~/.ansible/tmp`, set writable temp paths:

```bash
mkdir -p .ansible/tmp
export ANSIBLE_LOCAL_TEMP="$PWD/.ansible/tmp"
export ANSIBLE_REMOTE_TMP="$PWD/.ansible/tmp"
```

---

## Author
- Automation Development Office

---

## Repository layout (role)

```text
roles/
└─ utilities_build_execution_environment/
   ├─ README.md
   ├─ defaults/
   │  └─ main.yml
   ├─ meta/
   │  ├─ main.yml
   │  └─ argument_specs.yml
   ├─ tasks/
   │  └─ main.yml
   └─ templates/
      ├─ execution-environment.yml.j2
      └─ requirements.yml.j2
```
