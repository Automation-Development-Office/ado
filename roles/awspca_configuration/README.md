# Role: `awspca_configuration`

Manage an AWS PCA-backed `AWSPCAClusterIssuer` and its credentials Secret in OpenShift/Kubernetes.

This role supports `present` and `absent` state flows and can optionally wait for issuer readiness.

## Role Author

Chad Elliott

## ✅ Role Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- AWS PCA issuer CRDs installed before running the role.
- AWS credentials available by role variables or environment variables.

## 📦 Role Variables

| Variable | Description | Required | Default |
| -------- | ----------- | -------- | ------- |
| `state` | Desired state for resources. Supported values: `present`, `absent`. | Yes | N/A |
| `awspca_configuration_namespace` | Namespace where the AWS credentials Secret exists. | No | `cert-manager` |
| `awspca_configuration_secret_name` | Secret name that stores AWS credentials. | No | `awspca-creds` |
| `awspca_configuration_issuer_name` | Name of the `AWSPCAClusterIssuer` resource. | No | `awspca-clusterissuer` |
| `awspca_configuration_region` | AWS region used by the issuer. | No | `us-gov-west-1` |
| `awspca_configuration_pca_arn` | Private CA ARN used by `AWSPCAClusterIssuer`. | Yes (`state: present`) | `""` |
| `awspca_configuration_access_key_id` | Explicit AWS access key ID. Falls back to `AWS_ACCESS_KEY_ID` env var when empty. | No | `""` |
| `awspca_configuration_secret_access_key` | Explicit AWS secret access key. Falls back to `AWS_SECRET_ACCESS_KEY` env var when empty. | No | `""` |
| `awspca_configuration_secret_key_id_field` | Secret key field name for access key ID in Kubernetes Secret `stringData`. | No | `AWS_ACCESS_KEY_ID` |
| `awspca_configuration_secret_secret_key_field` | Secret key field name for secret access key in Kubernetes Secret `stringData`. | No | `AWS_SECRET_ACCESS_KEY` |
| `awspca_configuration_wait_ready` | Wait for issuer Ready condition after creation. | No | `true` |
| `awspca_configuration_wait_retries` | Retry count for readiness polling. | No | `30` |
| `awspca_configuration_wait_delay` | Delay (seconds) between readiness polling attempts. | No | `10` |
| `awspca_configuration_no_log` | Hide sensitive values in task output. | No | `true` |

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.awspca_configuration
      vars:
        state: present
        awspca_configuration_namespace: cert-manager
        awspca_configuration_secret_name: awspca-creds
        awspca_configuration_issuer_name: awspca-clusterissuer
        awspca_configuration_region: us-gov-west-1
        awspca_configuration_pca_arn: arn:aws-us-gov:acm-pca:region:account:certificate-authority/example
```

## 🧪 Role Molecule Testing

This role includes a Molecule scenario under `molecule/default/`.

Run from the role directory:

```bash
molecule test -s default
```

## 📁 Role Structure

```text
awspca_configuration/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── molecule/
│   └── default/
│       ├── converge.yml
│       ├── destroy.yml
│       ├── molecule.yml
│       ├── README.md
│       ├── TEST.md
│       └── verify.yml
├── README.md
├── tasks/
│   └── main.yml
├── tests/
│   └── inventory
└── vars/
    └── main.yml
```
