# Role: infra.ado.grafana_manage_folders

This role manages Grafana folders through the `grafana.grafana.folder`
module using canonical `grafana_manage_folders_*` variables.

## Requirements

- Network access from the Ansible controller to the Grafana API endpoint.
- `grafana.grafana` collection available for `folder` operations.
- A Grafana API key with permission to create/update folders.

## Variables

| Variable | Default | Description |
| --- | --- | --- |
| `grafana_manage_folders_state` | `present` | Desired folder state. |
| `grafana_manage_folders_name` | `General` | Folder title and UID prefix (`<name>-folder`). |
| `grafana_manage_folders_hostname` | `""` | Grafana hostname (without scheme). |
| `grafana_manage_folders_api_key` | `""` | Grafana API key used by `grafana.grafana.folder`. |
| `grafana_manage_folders_overwrite` | `true` | Whether folder updates overwrite existing definition. |

### Compatibility aliases

The role accepts these compatibility aliases:

- `state` -> `grafana_manage_folders_state`
- `grafana_folder` -> `grafana_manage_folders_name`
- `grafana_hostname` -> `grafana_manage_folders_hostname`
- `grafana_api_key` -> `grafana_manage_folders_api_key`
- `grafana_admin_password` -> `grafana_manage_folders_api_key` (legacy fallback)
- `grafana_folder_overwrite` -> `grafana_manage_folders_overwrite`

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
        grafana_manage_folders_api_key: "{{ vault_grafana_api_key }}"
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
