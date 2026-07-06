# Role: infra.ado.ocp_ldap_auth

Ocp Ldap Auth automation role. Primary tasks include: Assert ldap_config is present (from vault); Build ocp_ldap_auth_config from ldap_config (vault) + optional overrides; Skip when LDAP auth disabled.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_ldap_auth_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_ldap_auth
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_ldap_auth
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Assert ldap_config is present (from vault)
- Build ocp_ldap_auth_config from ldap_config (vault) + optional overrides
- Skip when LDAP auth disabled
- Assert required LDAP fields

```bash
cd roles/ocp_ldap_auth
molecule test
```

## 📁 Role Structure

```text
roles/ocp_ldap_auth/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
