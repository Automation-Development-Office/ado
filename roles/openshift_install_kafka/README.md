# Role: openshift_install_kafka

Complete Kafka operator installation flow and optionally create a Kafka custom resource.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- Operator catalog access for resolving the Kafka CSV.

---

## Variables

| Variable | Description |
|---------|-------------|
| `operator_name / operator_channel / operator_source_namespace` | Inputs used to resolve the current CSV for the operator. |
| `operator_subscription_namespace` | Namespace where the operator is installed. Defaults to `openshift-operators`. |
| `name_space` | Operand namespace for Kafka resources. Defaults to `cfk-operator`. |
| `kafka_create_cr` | Boolean toggle to create a minimal Kafka CR after operator readiness. |
| `kafka_cluster_name / kafka_replicas / kafka_data_volume_capacity` | Optional settings for the Kafka CR. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_install_kafka
      vars:
        operator_name: confluent-for-kubernetes
        operator_channel: stable
        operator_source_namespace: openshift-marketplace
        operator_subscription_namespace: openshift-operators
        name_space: cfk-operator
        kafka_create_cr: true
        kafka_cluster_name: kafka-cluster
```

---

## Behavior Notes

- Resolves the effective CSV, waits for operator readiness, and can optionally create a Kafka CR.
- When the CR is created, the role also waits for operand pods to appear and become Running.

---

## Molecule

Use the same README layout as the working collection roles so Molecule/README validation sees the expected sections and ordering.

```
dependency -> lint -> syntax -> create -> converge -> idempotence -> destroy -> verify
```

---

## License

GPL-3.0-or-later

---

## Author

Chad Elliott

---

## Repository layout (role)

```text
roles/
`-- openshift_install_kafka/
    |-- README.md
    |-- defaults/
    |   `-- main.yml
    |-- tasks/
    |   `-- main.yml
    |-- vars/
    |   `-- main.yml
    |-- handlers/
    |   `-- main.yml
    |-- meta/
    |   `-- main.yml
    |-- templates/                # optional
    |-- files/                    # optional
    `-- tests/
        |-- inventory
        `-- test.yml               # optional
```
