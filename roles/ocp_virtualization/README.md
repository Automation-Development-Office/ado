# Role: infra.ado.ocp_virtualization

Ocp Virtualization automation role. Primary tasks include: Ensure required variables are defined; Create a VirtualMachine by cloning the existing datavolume; Wait until the VirtualMachine is started.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_virtualization_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run ocp_virtualization
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_virtualization
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Ensure required variables are defined
- Create a VirtualMachine by cloning the existing datavolume
- Wait until the VirtualMachine is started
- Create OpenShift VirtualMachine

```bash
cd roles/ocp_virtualization
molecule test
```

## 📁 Role Structure

```text
roles/ocp_virtualization/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
