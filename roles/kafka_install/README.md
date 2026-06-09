# Role: infra.ado.kafka_install

Complete Kafka operator installation flow and optionally create a Kafka custom resource.

---

## Role Author

- Chad Elliott
- Automation Development Office

---

## Role Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- Operator catalog access for resolving the Kafka CSV.

---

## Role Variables

| Variable | Description |
|---------|-------------|
| `operator_name / operator_channel / operator_source_namespace` | Inputs used to resolve the current CSV for the operator. |
| `operator_subscription_namespace` | Namespace where the operator is installed. Defaults to `openshift-operators`. |
| `name_space` | Operand namespace for Kafka resources. Defaults to `cfk-operator`. |
| `kafka_install_create_cr` | Boolean toggle to create a minimal Kafka CR after operator readiness. |
| `kafka_install_cluster_name / kafka_install_replicas / kafka_install_data_volume_capacity` | Optional settings for the Kafka CR. |

### Auth via environment

Set kube auth via environment before running Molecule or playbooks:

```bash
export K8S_AUTH_HOST="https://api.ocp.example:6443"
export K8S_AUTH_API_KEY="..."
export K8S_AUTH_VERIFY_SSL="no"
```

---

## Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.kafka_install
      vars:
        operator_name: confluent-for-kubernetes
        operator_channel: stable
        operator_source_namespace: openshift-marketplace
        operator_subscription_namespace: openshift-operators
        name_space: cfk-operator
        kafka_install_create_cr: true
        kafka_install_cluster_name: kafka-cluster
```

---

### Behavior Notes

- Resolves the effective CSV, waits for operator readiness, and can optionally create a Kafka CR.
- When the CR is created, the role also waits for operand pods to appear and become Running.

---

## Role Molecule Testing

The Molecule scenario lives at `extensions/molecule/kafka_install`.

CI runs the `verify` stage to validate this README and role layout. Full cluster
integration (converge, idempotence, destroy) requires OpenShift credentials via
`K8S_AUTH_*` environment variables.

Run from the extensions Molecule directory:

```bash
cd extensions/molecule
ln -sfn . molecule
molecule test -s kafka_install
```

For full integration against a cluster:

```bash
export K8S_AUTH_HOST="https://api.ocp.example:6443"
export K8S_AUTH_API_KEY="..."
export K8S_AUTH_VERIFY_SSL="no"
molecule converge -s kafka_install
molecule idempotence -s kafka_install
molecule verify -s kafka_install
molecule destroy -s kafka_install
```

---

## Role Structure

```text
kafka_install/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   └── main.yml
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/
    └── main.yml
```

---

## License

GPL-3.0-or-later
