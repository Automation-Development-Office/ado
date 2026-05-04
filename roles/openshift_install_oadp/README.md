# Role: openshift_install_oadp

Configure an OADP `DataProtectionApplication` and related STS-backed backup resources.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- OADP operator installed before this role runs.
- AWS bucket and region values available when configuring backups.

---

## Variables

| Variable | Description |
|---------|-------------|
| `oadp_configure` | Boolean toggle for the configuration workflow. |
| `name_space` | Namespace where OADP resources are managed. |
| `cluster_id` | Cluster identifier used to name the DataProtectionApplication and backup prefix. |
| `aws_backup_bucket / aws_region` | S3 bucket and region for backup storage. |
| `oadp_iam_role_arn` | Optional STS IAM role ARN used for cloud credentials and service account annotation. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_install_oadp
      vars:
        oadp_configure: true
        name_space: openshift-adp
        cluster_id: prod-cluster
        aws_backup_bucket: my-oadp-backups
        aws_region: us-east-1
        oadp_iam_role_arn: arn:aws:iam::123456789012:role/oadp-role
```

---

## Behavior Notes

- Creates a `DataProtectionApplication` and optional STS secret/annotation when configuration is enabled.
- Waits for Velero, node-agent, and backup storage location readiness.

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
`-- openshift_install_oadp/
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
