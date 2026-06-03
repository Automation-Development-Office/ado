# Role: infra.ado.applications_grafana_manage_folder

This role manages Grafana folders through the `community.grafana.grafana_folder`
module using canonical `applications_grafana_manage_folder_*` variables.

## Requirements

- Network access from the Ansible controller to the Grafana API endpoint.
- `community.grafana` collection available for `grafana_folder` operations.
- Valid Grafana admin credentials.

## Variables

| Variable | Default | Description |
| --- | --- | --- |
| `applications_grafana_manage_folder_state` | `present` | Desired folder state. |
| `applications_grafana_manage_folder_name` | `General` | Folder title and UID prefix (`<name>-folder`). |
| `applications_grafana_manage_folder_hostname` | `""` | Grafana hostname (without scheme). |
| `applications_grafana_manage_folder_admin_user` | `""` | Grafana admin username. |
| `applications_grafana_manage_folder_admin_password` | `""` | Grafana admin password. |
| `applications_grafana_manage_folder_validate_certs` | `false` | Whether to validate Grafana TLS certificates. |

### Compatibility aliases

The role still accepts legacy aliases and normalizes them internally:

- `state` -> `applications_grafana_manage_folder_state`
- `grafana_folder` -> `applications_grafana_manage_folder_name`
- `grafana_hostname` -> `applications_grafana_manage_folder_hostname`
- `grafana_admin_user` -> `applications_grafana_manage_folder_admin_user`
- `grafana_admin_password` -> `applications_grafana_manage_folder_admin_password`
- `grafana_validate_certs` -> `applications_grafana_manage_folder_validate_certs`

## Example

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.applications_grafana_manage_folder
      vars:
        applications_grafana_manage_folder_state: present
        applications_grafana_manage_folder_name: Platform
        applications_grafana_manage_folder_hostname: grafana.example.com
        applications_grafana_manage_folder_admin_user: admin
        applications_grafana_manage_folder_admin_password: "{{ vault_grafana_admin_password }}"
```

## Molecule

This role uses an extension-level integration scenario:

- `extensions/molecule/integration_applications_grafana_manage_folder/molecule.yml`

Shared playbooks are located at:

- `extensions/molecule/utils/playbooks/applications_grafana_manage_folder_prepare.yml`
- `extensions/molecule/utils/playbooks/applications_grafana_manage_folder_converge.yml`
- `extensions/molecule/utils/playbooks/applications_grafana_manage_folder_verify.yml`
- `extensions/molecule/utils/playbooks/applications_grafana_manage_folder_destroy.yml`

Run from `extensions/molecule`:

```bash
molecule test -s integration_applications_grafana_manage_folder
```
