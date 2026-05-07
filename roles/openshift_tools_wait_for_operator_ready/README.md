# Role: openshift_tools_wait_for_operator_ready

Wait for an operator CSV and deployment to become available in a target namespace.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.

---

## Variables

| Variable | Description |
|---------|-------------|
| `name_space` | Namespace where the operator is installed. Required. |
| `operator_name_substring` | Substring used to identify the operator CSV. Required. |
| `operator_poll_interval / operator_install_timeout` | CSV polling interval and overall install timeout values. |
| `operator_wait_retries / operator_wait_delay` | Deployment readiness polling values. |
| `wait_for_operator_ready_operator_deployment_pattern` | Optional deployment name pattern override. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_tools_wait_for_operator_ready
      vars:
        name_space: openshift-operators
        operator_name_substring: cert-manager
        operator_poll_interval: 10
        operator_install_timeout: 900
```

---

## Behavior Notes

- Waits first for a matching CSV to appear, then discovers and waits on the matching deployment.
- Publishes debug messages that show both the CSV and deployment readiness status.

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
`-- openshift_tools_wait_for_operator_ready/
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
