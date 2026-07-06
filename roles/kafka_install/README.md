# Role: infra.ado.kafka_install

Kafka Install automation role. Primary tasks include: Kafka Install Set derived vars; Kafka Install Lookup currentCSV for channel when operator_starting_csv not provided; Kafka Install Derive effective starting CSV (safe).

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `kafka_install_state` | Desired state used by role tasks when supported. |

## 🚀 Role Usage

```yaml
- name: Run kafka_install
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.kafka_install
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Kafka Install Set derived vars
- Kafka Install Lookup currentCSV for channel when operator_starting_csv not provided
- Kafka Install Derive effective starting CSV (safe)
- Kafka Install Set kafka_install_operator_starting_csv_effective from provided startingCSV

```bash
cd roles/kafka_install
molecule test
```

## 📁 Role Structure

```text
roles/kafka_install/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
