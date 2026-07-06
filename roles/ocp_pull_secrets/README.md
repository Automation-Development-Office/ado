# Role: infra.ado.ocp_pull_secrets

Ocp Pull Secrets automation role. Primary tasks include: Assert state is provided via -e or AAP survey; Normalize state; Set defaults for pull secret target.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_pull_secrets_name` | Resource name used by this role. |
| `ocp_pull_secrets_namespace` | OpenShift namespace value used by this role. |
| `ocp_pull_secrets_registry_host` | Endpoint or host value used by this role. |
| `ocp_pull_secrets_registry_username` | Resource name used by this role. |
| `ocp_pull_secrets_registry_password` | Sensitive credential value used by this role. |

## 🚀 Role Usage

```yaml
- name: Run ocp_pull_secrets
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_pull_secrets
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Assert state is provided via -e or AAP survey
- Normalize state
- Set defaults for pull secret target
- Read current pull-secret

```bash
cd roles/ocp_pull_secrets
molecule test
```

## 📁 Role Structure

```text
roles/ocp_pull_secrets/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
