# Role: ado.utilities_build_execution_environment

Build a custom Ansible **Execution Environment (EE)** image with `ansible-builder`.

- Uses a caller-provided base EE image
- Pulls the base image from a caller-provided source repository
- Adds caller-provided collections during the EE build

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
| `utilities_build_execution_environment_collections` | List of Ansible collections to include in the EE image. **Required.** |
| `utilities_build_execution_environment_output_image` | Output image name and tag for the built EE. Default: `custom-ee:latest`. |
| `utilities_build_execution_environment_build_context` | Build context directory used by `ansible-builder`. Default: `/tmp/utilities_build_execution_environment`. |
| `utilities_build_execution_environment_builder_executable` | `ansible-builder` executable name or full path. Default: `ansible-builder`. |
| `utilities_build_execution_environment_package_manager_path` | Package manager path inside the base image used by `ansible-builder` (for example `/usr/bin/microdnf` or `/usr/bin/dnf`). Default: `/usr/bin/microdnf`. |

### Auth via environment (optional)

No role-specific environment authentication variables are required by this role.

---

## Examples

### Build a custom EE image
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.utilities_build_execution_environment
      vars:
        utilities_build_execution_environment_base_ee: ee-minimal-rhel9:latest
        utilities_build_execution_environment_source_image_repository: registry.redhat.io/ansible-automation-platform-24
        utilities_build_execution_environment_collections:
          - ansible.posix
          - kubernetes.core
        utilities_build_execution_environment_output_image: localhost/custom-ee:latest
```

### Build with a custom context directory
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.utilities_build_execution_environment
      vars:
        utilities_build_execution_environment_base_ee: ee-supported-rhel9:latest
        utilities_build_execution_environment_source_image_repository: quay.io/ansible
        utilities_build_execution_environment_collections:
          - community.general
        utilities_build_execution_environment_build_context: /tmp/ee-build-demo
        utilities_build_execution_environment_output_image: localhost/custom-ee:demo
```

---

## Behavior Notes

- The role composes the base image reference from repository + base EE image.
- It renders `execution-environment.yml` and `requirements.yml` into the build context.
- It runs `ansible-builder build` using the rendered files and selected output tag.
- It sets `options.package_manager_path` in the EE definition to match the selected base image.
- Required inputs are enforced by role argument specs and runtime assertions.

---

## Molecule

No role-local Molecule scenario is currently defined for this role.

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
