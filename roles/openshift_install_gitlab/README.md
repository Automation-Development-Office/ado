# Role: ado.openshift.gitlab

Install and configure GitLab on OpenShift using the GitLab Operator and Custom Resource (CR). The role:
- Creates Kubernetes Secrets for TLS, root password, and Postgres credentials.
- Deploys the GitLab Operator CR with all required references and settings.
- Supports idempotent updates and safe deletion.
- Uses **Ansible Vault** for storing sensitive secrets (root and DB passwords).

---

## Requirements

- OpenShift API reachable with auth (`K8S_AUTH_*` env vars or module params)
- Collections:
  - `kubernetes.core`
- GitLab Operator installed and CRDs available in the target cluster
- Secrets managed with Ansible Vault
- Optional CLIs for verification: `oc`, `kubectl`, `jq`

---

## Variables

### Top-level

| Variable        | Description                                       |
|-----------------|---------------------------------------------------|
| `name_space`    | Namespace to deploy GitLab and all resources      |
| `validate_certs`| TLS verification for k8s modules. Default `false` |

### GitLab Instance

| Variable              | Default    | Meaning                                      |
|-----------------------|------------|----------------------------------------------|
| `gitlab_hostname`     | —          | Hostname for GitLab (used in Route/service)  |
| `gitlab_storage_size` | —          | Size for GitLab persistent volume            |
| `storage`             | —          | StorageClass for GitLab persistent volume    |
| `tls_crt`             | —          | TLS certificate for HTTPS endpoint           |
| `tls_key`             | —          | TLS private key for HTTPS endpoint           |

### Secrets (use Ansible Vault)

| Variable                | Default | Notes                                   |
|-------------------------|---------|-----------------------------------------|
| `gitlab_admin_user`     | admin   | GitLab DB/Postgres admin username       |
| `gitlab_admin_password` | —       | GitLab DB/Postgres admin password       |
| `gitlab_root_password`  | —       | GitLab root (web UI) password           |

> **Notes**
> - Passwords should be stored in Ansible Vault (`group_vars/all/vault.yml` or similar)
> - TLS data should be provided as variables or loaded from files

---

## Examples

### Minimal

```yaml
- hosts: localhost
  gather_facts: false
  vars_files:
    - group_vars/all/vault.yml
  vars:
    name_space: gitlab
    gitlab_hostname: "gitlab.apps.example.com"
    gitlab_storage_size: "20Gi"
    storage: "gp2-csi"
    tls_crt: "{{ lookup('file', 'files/gitlab.crt') }}"
    tls_key: "{{ lookup('file', 'files/gitlab.key') }}"
  roles:
    - ado.openshift.gitlab
```

### Vaulted secrets

```yaml
# group_vars/all/vault.yml (encrypted with ansible-vault)
gitlab_admin_user: admin
gitlab_admin_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  ...encrypted data...
gitlab_root_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  ...encrypted data...
```

---

## Outputs

- GitLab Route/hostname for access
- Passwords are **never logged** (`no_log: true`)
- All resources are idempotently updated or created

---

## Behavior Notes

- All referenced secrets and config created before the Custom Resource.
- The chart version is set to a **supported version** (e.g. `9.4.0`). Change in `tasks/main.yml` if needed.
- The operator CR is updated if settings change.
- For deletion, use the appropriate delete task in `tasks/delete-gitlab-operator.yml`.

---

## Troubleshooting

- If the CR fails to create, check error message for supported chart version.
- Ensure all referenced Secrets exist and are properly formatted.
- Check Pod logs for container startup errors (e.g. database connectivity, TLS).
- For vault problems, verify your secrets are loaded and decrypted correctly.

---

## Molecule

A default Molecule scenario is provided under `molecule/default` and covers:
- Resource creation and update
- Secret management
- Custom Resource deployment
- Proper deletion and cleanup

Set kube auth via environment:

```bash
export K8S_AUTH_HOST="https://api.ocp.example:6443"
export K8S_AUTH_API_KEY="…"
export K8S_AUTH_VERIFY_SSL="no"
```

Run:

```bash
molecule converge
molecule idempotence
molecule verify
molecule destroy
```

Your `molecule.yml` wires `converge`, `verify`, and `destroy` to their respective playbooks.

---

## Author

- Chad Elliott (<chelliot@redhat.com>)

---

## Repository layout

```text
.
├── defaults
│   └── main.yml
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── molecule
│   └── default
│       ├── converge.yml
│       ├── destroy.yml
│       ├── molecule.yml
│       ├── README.md
│       ├── TEST.md
│       └── verify.yml
├── README.md
├── tasks
│   ├── delete-gitlab-operator.yml
│   ├── install-gitlab-operator.yml
│   └── main.yml
├── tests
│   ├── inventory
```
