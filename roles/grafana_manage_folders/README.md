# Role: infra.ado.grafana_manage_folders

This role manages Grafana folders with `grafana.grafana.folder`.

It normalizes input into canonical `grafana_manage_folders_*` variables and then
creates or updates a folder when the resolved state is `present`.

## Requirements

- `grafana.grafana` collection (module: `grafana.grafana.folder`)

Example install:

```bash
ansible-galaxy collection install grafana.grafana
```

## Variables

This role currently resolves values in `tasks/main.yml` (there is no
`defaults/main.yml` in the role path). Effective fallback values are:

| Canonical variable | Effective fallback | Description |
| --- | --- | --- |
| `grafana_manage_folders_state` | `present` | Desired folder state. |
| `grafana_manage_folders_name` | `General` | Folder title and UID prefix (`<name>-folder`). |
| `grafana_manage_folders_hostname` | `""` | Grafana hostname (without scheme). |
| `grafana_manage_folders_api_key` | `""` | Grafana API key used by `grafana.grafana.folder`. |
| `grafana_manage_folders_overwrite` | `true` | Whether updates overwrite existing folder definition. |

### Compatibility aliases

Normalization accepts these aliases before applying fallback values:

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
        grafana_manage_folders_overwrite: true
```

## Molecule

Extension-level scenario:

- `extensions/molecule/integration_grafana_manage_folders/molecule.yml`

Shared playbooks:

- `extensions/molecule/utils/playbooks/grafana_manage_folders_prepare.yml`
- `extensions/molecule/utils/playbooks/grafana_manage_folders_converge.yml`
- `extensions/molecule/utils/playbooks/grafana_manage_folders_verify.yml`
- `extensions/molecule/utils/playbooks/grafana_manage_folders_destroy.yml`

Run from `extensions/molecule`:

```bash
molecule test -s integration_grafana_manage_folders
```
