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
