# Role: infra.ado.ocp_oidc_auth

Ocp Oidc Auth automation role. Primary tasks include: Assert required OIDC inputs are set; Build Keycloak URLs; Try to get Keycloak client secret via module.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_oidc_auth_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_oidc_auth
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_oidc_auth
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Assert required OIDC inputs are set
- Build Keycloak URLs
- Try to get Keycloak client secret via module
- Extract Keycloak client secret from module result

```bash
cd roles/ocp_oidc_auth
molecule test
```

## 📁 Role Structure

```text
roles/ocp_oidc_auth/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
