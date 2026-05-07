# Role: openshift_configure_logging

Configure an OpenShift `ClusterLogForwarder` and optional Splunk secret for cluster logging.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- OpenShift Logging operator installed before this role runs.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Outer guard used by the role. Use `present` for the current create path. |
| `cluster_forwarder_state` | State applied to the secret and ClusterLogForwarder resources. |
| `name_space` | Namespace where the log forwarder is managed. Required. |
| `cluster_forwarder_name` | Name of the ClusterLogForwarder resource. |
| `cluster_forwarder_secret / cluster_forwarder_secret_key` | Secret name and key used for Splunk token authentication. |
| `splunk_url / splunk_logging_name / splunk_secret` | Splunk endpoint configuration and optional HEC token secret content. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_logging
      vars:
        state: present
        cluster_forwarder_state: present
        name_space: openshift-logging
        cluster_forwarder_name: instance
        cluster_forwarder_secret: vector-splunk-secret
        cluster_forwarder_secret_key: hecToken
        splunk_url: https://splunk.example.com
        splunk_logging_name: splunk-audit
        splunk_secret: "{{ vault_splunk_hec_token }}
```

---

## Behavior Notes

- Creates the Splunk secret when `splunk_secret` is provided.
- Applies a `ClusterLogForwarder` configured to ship audit logs to Splunk.

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
`-- openshift_configure_logging/
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
