# Role: infra.ado.ocp_htpasswd_admin

Ocp Htpasswd Admin automation role. Primary tasks include: Build htpasswd content from user list; Create htpasswd Secret; Grant cluster-admin to selected htpasswd users.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_htpasswd_admin_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_htpasswd_admin
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_htpasswd_admin
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Build htpasswd content from user list
- Create htpasswd Secret
- Grant cluster-admin to selected htpasswd users
- Get current OAuth config

```bash
cd roles/ocp_htpasswd_admin
molecule test
```

## 📁 Role Structure

```text
roles/ocp_htpasswd_admin/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
