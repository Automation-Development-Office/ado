# Role: infra.ado.ocp_iscsi_storage

Ocp Iscsi Storage automation role. Primary tasks include: Get all storage classes; Set fact if default storage class exists; Create synology-csi namespace.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_iscsi_storage_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_iscsi_storage
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_iscsi_storage
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Get all storage classes
- Set fact if default storage class exists
- Create synology-csi namespace
- Create client-info-secret from file

```bash
cd roles/ocp_iscsi_storage
molecule test
```

## 📁 Role Structure

```text
roles/ocp_iscsi_storage/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
