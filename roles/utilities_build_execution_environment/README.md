# Role: `utilities_build_execution_environment`

This role builds a custom Ansible execution environment (EE) image with `ansible-builder`.

The end user provides:
- The base EE image name and tag to start from.
- The source image repository path to pull that base EE image from.
- The list of collections to include in the built EE image.

## Requirements

- Ansible >= 2.14
- `ansible-builder` available on the managed host where the role runs
- Container runtime dependencies required by `ansible-builder`

## Required Variables

The following variables are required by this role and enforced through role argument specs:

- `utilities_build_execution_environment_base_ee`
- `utilities_build_execution_environment_source_image_repository`
- `utilities_build_execution_environment_collections`

## Optional Variables

- `utilities_build_execution_environment_output_image` (default: `custom-ee:latest`)
- `utilities_build_execution_environment_build_context` (default: `/tmp/utilities_build_execution_environment`)
- `utilities_build_execution_environment_builder_executable` (default: `ansible-builder`)

## Example Playbook

```yaml
- name: Build custom execution environment
  hosts: localhost
  gather_facts: false
  vars:
    utilities_build_execution_environment_base_ee: "ee-minimal-rhel9:latest"
    utilities_build_execution_environment_source_image_repository: "registry.redhat.io/ansible-automation-platform-24"
    utilities_build_execution_environment_collections:
      - "ansible.posix"
      - "kubernetes.core"
    utilities_build_execution_environment_output_image: "localhost/custom-ee:latest"
  roles:
    - role: ado.utilities_build_execution_environment
```
