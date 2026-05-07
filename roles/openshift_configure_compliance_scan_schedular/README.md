# Role: openshift_configure_compliance_scan_schedular

Create Compliance Operator scan resources for scheduled or immediate scan execution.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- Compliance Operator CRDs installed in the target cluster.

---

## Variables

| Variable | Description |
|---------|-------------|
| `schedule_scan` | Boolean toggle to create a `ComplianceScan` resource. |
| `run_scan` | Boolean toggle to create a `ComplianceSuite` resource. |
| `compliance_scan_name` | Name of the `ComplianceScan` resource. |
| `compliance_suite_name` | Name of the `ComplianceSuite` resource. |
| `compliance_profile` | Compliance profile referenced by the scan. |
| `compliance_operator_namespace` | Namespace for the Compliance Operator resources. Defaults to `openshift-compliance`. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_compliance_scan_schedular
      vars:
        schedule_scan: true
        run_scan: true
        compliance_scan_name: daily-node-scan
        compliance_suite_name: daily-suite
        compliance_profile: ocp4-cis
        compliance_operator_namespace: openshift-compliance
```

---

## Behavior Notes

- Creates a `ComplianceScan` when `schedule_scan` is enabled.
- Creates a `ComplianceSuite` when `run_scan` is enabled.

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
`-- openshift_configure_compliance_scan_schedular/
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
