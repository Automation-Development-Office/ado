# Role: infra.ado.bootstrap_generate_env_vars

Generate environment group variables and vault files used by the ADO bootstrap
playbook repository.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- `env` set to the target environment
- A vault password file when encrypted vault files are enabled
- Optional preflight JSON from the ADO preflight UI or CLI
- Write access to the bootstrap playbook repository working tree

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `env` | Target environment directory under `group_vars/all`. |
| `preflight_json` | Optional JSON file containing UI or CLI preflight answers. |
| `generate_env_vars_base_dir` | Base directory for generated environment variables. |
| `generate_env_vars_create_dirs` | Creates bootstrap repository directories when true. |
| `generate_env_vars_encrypt_vault_files` | Encrypts generated vault files when true. |
| `generate_env_vars_components` | Component list for generated `vars_*.yml` and `vault_*.yml` files. |
| `generate_env_vars_force` | Allows generated files to be overwritten. |
| `generate_env_vars_force_overwrite` | Compatibility overwrite flag mapped to `generate_env_vars_force`. |
| `bootstrap_generate_env_vars_machine_credential_enabled` | Creates an AAP Machine credential when using CLI vars without `preflight_json`. |
| `bootstrap_generate_env_vars_machine_credential_name` | AAP Machine credential name. Default `<org>-machine`. Custom names are normalized to the organization prefix. |
| `bootstrap_generate_env_vars_machine_credential_username` | SSH username for the Machine credential. Default `cloud-user`. |
| `bootstrap_generate_env_vars_machine_credential_ssh_key_data` | SSH private key data written to `vault_machine_cred.yml`. |
| `bootstrap_generate_env_vars_machine_credential_ssh_key_unlock` | Optional SSH private key passphrase written to `vault_machine_cred.yml`. |
| `bootstrap_generate_env_vars_machine_credential_become_method` | Become method for the Machine credential. Default `sudo`. |
| `bootstrap_generate_env_vars_machine_credential_become_username` | Become username for the Machine credential. Default `root`. |
| `bootstrap_generate_env_vars_aap_additional_credentials` | Additional AAP credentials to add to generated controller config. Secret-capable fields are written to `aap_vault.yml`. |
| `bootstrap_generate_env_vars_hub_publish_ado_collection` | Enables generated vars for adding the ADO collection to Automation Hub. Default `true`. |
| `bootstrap_generate_env_vars_hub_mark_ado_validated` | Targets the generated ADO collection hub entry at validated content when enabled. Default `true`. |
| `bootstrap_generate_env_vars_hub_ado_collection_path` | Local ADO collection path used by generated hub collection vars. Default `.`. |
| `bootstrap_generate_env_vars_satellite_server_url` | Satellite server URL written to `vars_satellite.yml`. |
| `bootstrap_generate_env_vars_satellite_organization` | Satellite organization written to `vars_satellite.yml`. |
| `bootstrap_generate_env_vars_satellite_service_account_username` | Satellite service account username used by `satellite_config`. |
| `bootstrap_generate_env_vars_satellite_service_account_password` | Satellite service account password written to `vault_satellite.yml`. |
| `bootstrap_generate_env_vars_satellite_admin_password` | Satellite admin password written to `vault_satellite.yml`; defaults to the service account password when omitted. |
| `bootstrap_generate_env_vars_satellite_validate_certs` | Satellite TLS validation setting. Default `false`. |
| `bootstrap_generate_env_vars_satellite_dynamic_inventory_enabled` | Creates a Satellite 6 dynamic inventory source in AAP when true. Default `false`; preflight JSON defaults to `true` when Satellite is selected and the setting is omitted. |
| `bootstrap_generate_env_vars_satellite_credential_name` | AAP credential name for the Satellite 6 inventory source. |
| `bootstrap_generate_env_vars_satellite_inventory_source_name` | AAP inventory source name for Satellite dynamic inventory. |
| `bootstrap_generate_env_vars_satellite_inventory_overwrite` | Overwrite hosts during Satellite inventory sync. Default `true`. |
| `bootstrap_generate_env_vars_satellite_inventory_overwrite_vars` | Overwrite host variables during Satellite inventory sync. Default `true`. |
| `bootstrap_generate_env_vars_satellite_inventory_update_on_launch` | Update the Satellite inventory source when launched. Default `true`. |
| `bootstrap_generate_env_vars_satellite_inventory_update_cache_timeout` | Cache timeout for the Satellite inventory source. Default `0`. |
| `bootstrap_generate_env_vars_satellite_inventory_host_filter` | Optional Satellite inventory source host filter. |

Generated AAP inventories are split by purpose:

- `<org>-inventory` contains only `localhost` for controller-side and local
  bootstrap jobs.
- `<org>-RHEL-Inventory` contains RHEL managed hosts supplied through the
  preflight form or CLI vars. Satellite dynamic inventory sources also attach
  to this inventory because Satellite-sourced hosts are managed RHEL targets.
- `<org>-IDM-Inventory` contains IDM server and replica hosts when IDM is
  selected.
- `<org>-Satellite-Server-Inventory` contains the Satellite server host when
  Satellite is selected.

Additional AAP credentials, the primary AAP Vault credential, the primary AAP
Machine credential, and Satellite dynamic inventory objects are normalized to
the organization-prefixed name pattern. For example, `IDM-Cred`,
`test-machine`, and `test-vault` under organization `RH` become `RH-IDM-Cred`,
`RH-test-machine`, and `RH-test-vault`.

Generated AAP project names are normalized the same way. If the organization is
`RH` and the project field is `test-project`, the generated AAP project becomes
`RH-test-project`.

Generated AAP labels include the organization name, for example `ADO`, plus
organization-prefixed component labels such as `ADO | rhel`,
`ADO | satellite`, and `ADO | bootstrap`. These labels are attached to the
generated automation so AAP can group and filter by organization and component.

Satellite dynamic inventory creates an AAP inventory source named like
`ADO-Satellite-Dynamic-Inventory` on the RHEL inventory. It is not a separate
inventory named `ADO Satellite Dynamic Inventory`; it is a source attached to
`ADO-RHEL-Inventory` so synced Satellite hosts become managed RHEL targets.

## 🚀 Role Usage

```yaml
- name: Generate bootstrap environment variables
  hosts: localhost
  gather_facts: false
  vars:
    env: prod
    preflight_json: ado-preflight-prod.json
  roles:
    - role: infra.ado.bootstrap_generate_env_vars
```

## 🧪 Role Molecule Testing

Validate with a sample preflight JSON and local bootstrap repository fixture.

```bash
ansible-lint --offline roles/bootstrap_generate_env_vars
yamllint roles/bootstrap_generate_env_vars/tasks
```

## 📁 Role Structure

```text
roles/bootstrap_generate_env_vars/
  defaults/main.yml
  tasks/main.yml
  README.md
```
