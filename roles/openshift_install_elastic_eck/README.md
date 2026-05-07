# Role: openshift_install_elastic_eck

Finish Elastic ECK operator setup and optionally create a minimal Elasticsearch custom resource.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- A compatible operator catalog source must be reachable by the cluster.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Desired state. Use `present` for the current setup path. |
| `operator_name / operator_channel / operator_source / operator_source_namespace` | OLM subscription inputs used to install the operator. |
| `operator_subscription_namespace` | Namespace where the operator is subscribed. Defaults to `eck-operator`. |
| `name_space` | Operand namespace used for Elasticsearch resources. Defaults to `elastic`. |
| `eck_create_elasticsearch_cr` | Boolean toggle to create an Elasticsearch CR after operator install. |
| `eck_cluster_name / eck_version / eck_replicas` | Optional Elasticsearch CR tuning values. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_install_elastic_eck
      vars:
        state: present
        operator_name: elasticsearch-eck-operator-certified
        operator_channel: stable
        operator_source: certified-operators
        operator_source_namespace: openshift-marketplace
        operator_subscription_namespace: eck-operator
        name_space: elastic
        eck_create_elasticsearch_cr: true
```

---

## Behavior Notes

- Uses the shared subscription role to install the operator.
- Waits for the CSV and operator deployment to become ready before creating an optional Elasticsearch CR.

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
`-- openshift_install_elastic_eck/
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
