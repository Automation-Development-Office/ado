# Role: infra.ado.grafana_manage_folders

This role manages Grafana folders through the `community.grafana.grafana_folder`
module using canonical `grafana_manage_folders_*` variables.

## Requirements

- Network access from the Ansible controller to the Grafana API endpoint.
- `community.grafana` collection available for `grafana_folder` operations.
- Valid Grafana admin credentials.

## Variables

| Variable | Default | Description |
| --- | --- | --- |
| `grafana_manage_folders_state` | `present` | Desired folder state. |
| `grafana_manage_folders_name` | `General` | Folder title and UID prefix (`<name>-folder`). |
| `grafana_manage_folders_hostname` | `""` | Grafana hostname (without scheme). |
| `grafana_manage_folders_admin_user` | `""` | Grafana admin username. |
| `grafana_manage_folders_admin_password` | `""` | Grafana admin password. |
| `grafana_manage_folders_validate_certs` | `false` | Whether to validate Grafana TLS certificates. |

### Compatibility aliases

The role still accepts legacy aliases and normalizes them internally:

- `applications_grafana_manage_folder_state` -> `grafana_manage_folders_state`
- `applications_grafana_manage_folder_name` -> `grafana_manage_folders_name`
- `applications_grafana_manage_folder_hostname` -> `grafana_manage_folders_hostname`
- `applications_grafana_manage_folder_admin_user` -> `grafana_manage_folders_admin_user`
- `applications_grafana_manage_folder_admin_password` -> `grafana_manage_folders_admin_password`
- `applications_grafana_manage_folder_validate_certs` -> `grafana_manage_folders_validate_certs`
- `state` -> `grafana_manage_folders_state`
- `grafana_folder` -> `grafana_manage_folders_name`
- `grafana_hostname` -> `grafana_manage_folders_hostname`
- `grafana_admin_user` -> `grafana_manage_folders_admin_user`
- `grafana_admin_password` -> `grafana_manage_folders_admin_password`
- `grafana_validate_certs` -> `grafana_manage_folders_validate_certs`

## Example

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.grafana_manage_folders
      vars:
        grafana_manage_folders_state: present
        grafana_manage_folders_name: Platform
        grafana_manage_folders_hostname: grafana.example.com
        grafana_manage_folders_admin_user: admin
        grafana_manage_folders_admin_password: "{{ vault_grafana_admin_password }}"
```

## Molecule

This role uses an extension-level integration scenario:

- `extensions/molecule/integration_grafana_manage_folders/molecule.yml`

Shared playbooks are located at:

- `extensions/molecule/utils/playbooks/grafana_manage_folders_prepare.yml`
- `extensions/molecule/utils/playbooks/grafana_manage_folders_converge.yml`
- `extensions/molecule/utils/playbooks/grafana_manage_folders_verify.yml`
- `extensions/molecule/utils/playbooks/grafana_manage_folders_destroy.yml`

Run from `extensions/molecule`:

```bash
molecule test -s integration_grafana_manage_folders
```
