# Role: infra.ado.install_aap

Install Aap automation role. Primary tasks include: Assert manifest path is provided; Upload subscription manifest to AAP Controller; Wait for controller API to be reachable.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `install_aap_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run install_aap
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.install_aap
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Assert manifest path is provided
- Upload subscription manifest to AAP Controller
- Wait for controller API to be reachable
- Create Automation Hub credential (token)

```bash
cd roles/install_aap
molecule test
```

## 📁 Role Structure

```text
roles/install_aap/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
