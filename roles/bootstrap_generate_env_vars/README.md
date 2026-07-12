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
| `bootstrap_generate_env_vars_machine_credential_name` | AAP Machine credential name. Default `ado-machine`. |
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
