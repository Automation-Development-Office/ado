# Role: openshift_configure_awspca

Manage an AWS PCA-backed `AWSPCAClusterIssuer` and the credentials Secret it depends on.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- AWS PCA issuer CRDs installed before running the role.
- AWS credentials available by variables or environment variables.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Desired state: `present` or `absent`. Required. |
| `awspca_namespace` | Namespace used for the AWS credentials Secret. Defaults to `cert-manager`. |
| `awspca_secret_name` | Secret name that stores AWS credentials. |
| `awspca_issuer_name` | Name of the `AWSPCAClusterIssuer` resource. |
| `awspca_region` | AWS region used for AWS PCA operations. |
| `awspca_pca_arn` | Private CA ARN. Required when `state: present`. |
| `awspca_access_key_id / awspca_secret_access_key` | Optional explicit credentials. Environment variables are used as fallback. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_awspca
      vars:
        state: present
        awspca_namespace: cert-manager
        awspca_secret_name: awspca-creds
        awspca_issuer_name: awspca-clusterissuer
        awspca_region: us-gov-west-1
        awspca_pca_arn: arn:aws-us-gov:acm-pca:region:account:certificate-authority/example
```

---

## Behavior Notes

- Creates the namespace-scoped credentials Secret and the cluster-scoped issuer resource.
- When `awspca_wait_ready` is enabled, the role waits for a `Ready=True` condition.
- The absent path removes both the issuer and the credentials Secret.

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
`-- openshift_configure_awspca/
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
