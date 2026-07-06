# Role: infra.ado.ocp_nfs_storage

Ocp Nfs Storage automation role. Primary tasks include: Ensure Helm repo for csi-driver-nfs is present; Install csi-driver-nfs with Helm; Assign privileged SCC to csi-nfs-node-sa.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_nfs_storage_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_nfs_storage
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_nfs_storage
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Ensure Helm repo for csi-driver-nfs is present
- Install csi-driver-nfs with Helm
- Assign privileged SCC to csi-nfs-node-sa
- Assign privileged SCC to csi-nfs-controller-sa

```bash
cd roles/ocp_nfs_storage
molecule test
```

## 📁 Role Structure

```text
roles/ocp_nfs_storage/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
