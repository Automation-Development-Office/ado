# Role: infra.ado.ocp_wait_pods

Ocp Wait Pods automation role. Primary tasks include: Importing namespace; Set default values for pod wait retries and delay (if not set); Wait for all pods in namespace to be running.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_wait_pods_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_wait_pods
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_wait_pods
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Importing namespace
- Set default values for pod wait retries and delay (if not set)
- Wait for all pods in namespace to be running

```bash
cd roles/ocp_wait_pods
molecule test
```

## 📁 Role Structure

```text
roles/ocp_wait_pods/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
