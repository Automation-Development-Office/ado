# Role: infra.ado.ocp_operator_subscription

Ocp Operator Subscription automation role. Primary tasks include: Subscription | Derive namespaces and names; Subscription | Assert required inputs; Namespace | Ensure subscription namespace exists.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_operator_subscription_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_operator_subscription
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_operator_subscription
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Subscription | Derive namespaces and names
- Subscription | Assert required inputs
- Namespace | Ensure subscription namespace exists
- Openshift_tools_operator_groups | Create/Update (scoped vs all namespaces)

```bash
cd roles/ocp_operator_subscription
molecule test
```

## 📁 Role Structure

```text
roles/ocp_operator_subscription/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
