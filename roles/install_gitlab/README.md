# Role: infra.ado.install_gitlab

Install and configure GitLab on OpenShift using the GitLab Operator and Custom Resource (CR).

- Creates Kubernetes Secrets for TLS, root password, and Postgres credentials
- Deploys the GitLab Operator CR with required references and settings
- Supports idempotent updates and safe deletion
- Uses **Ansible Vault** for storing sensitive secrets (root and DB passwords)

---

## Role Author

- Chad Elliott (<chelliot@redhat.com>)
- Automation Development Office

---

## ✅ Role Requirements

- OpenShift API reachable with auth (`K8S_AUTH_*` env vars or module params)
- Collections:
  - `kubernetes.core`
- GitLab Operator installed and CRDs available in the target cluster
- Secrets managed with Ansible Vault
- Optional CLIs for verification: `oc`, `kubectl`, `jq`

---

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `state` | Desired state (`present` to install, `absent` to remove). Default: `present`. |
| `name_space` | Namespace to deploy GitLab and all resources. **Required.** |
| `install_gitlab_validate_certs` | TLS verification for k8s modules. Default: `false`. |
| `install_gitlab_hostname` | Hostname for GitLab (used in Route/service). **Required when `state` is `present`.** |
| `install_gitlab_storage_size` | Size for GitLab persistent volume. **Required when `state` is `present`.** |
| `install_gitlab_storage_class` | StorageClass for GitLab persistent volume. **Required when `state` is `present`.** |
| `install_gitlab_tls_crt` | TLS certificate for HTTPS endpoint. **Required when `state` is `present`.** |
| `install_gitlab_tls_key` | TLS private key for HTTPS endpoint. **Required when `state` is `present`.** |
| `install_gitlab_admin_user` | GitLab DB/Postgres admin username. Default: `admin`. |
| `install_gitlab_admin_password` | GitLab DB/Postgres admin password. **Required when `state` is `present`.** |
| `install_gitlab_root_password` | GitLab root (web UI) password. **Required when `state` is `present`.** |
| `install_gitlab_chart_version` | GitLab chart version for the operator CR. Default: `9.4.0`. |

### Auth via environment (optional)

Set kube auth via environment before running Molecule or playbooks:

```bash
export K8S_AUTH_HOST="https://api.ocp.example:6443"
export K8S_AUTH_API_KEY="…"
export K8S_AUTH_VERIFY_SSL="no"
```

> **Notes**
> - Passwords should be stored in Ansible Vault (`group_vars/all/vault.yml` or similar)
> - TLS data should be provided as variables or loaded from files

---

## 🚀 Role Usage

### Minimal install

```yaml
- hosts: localhost
  gather_facts: false
  vars_files:
    - group_vars/all/vault.yml
  vars:
    name_space: gitlab
    install_gitlab_hostname: "gitlab.apps.example.com"
    install_gitlab_storage_size: "20Gi"
    install_gitlab_storage_class: "gp2-csi"
    install_gitlab_tls_crt: "{{ lookup('file', 'files/gitlab.crt') }}"
    install_gitlab_tls_key: "{{ lookup('file', 'files/gitlab.key') }}"
  roles:
    - role: infra.ado.install_gitlab
```

### Vaulted secrets

```yaml
# group_vars/all/vault.yml (encrypted with ansible-vault)
install_gitlab_admin_user: admin
install_gitlab_admin_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  ...encrypted data...
install_gitlab_root_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  ...encrypted data...
```

### Uninstall

```yaml
- hosts: localhost
  gather_facts: false
  vars:
    name_space: gitlab
    state: absent
  roles:
    - role: infra.ado.install_gitlab
```

---

### Behavior Notes

- All referenced secrets and config are created before the Custom Resource.
- The chart version defaults to a supported version (`9.4.0`). Override with `install_gitlab_chart_version` if needed.
- The operator CR is updated if settings change.
- Passwords are **never logged** (`no_log: true`).
- For deletion, the role removes the GitLab CR, PostgreSQL resources, and secrets.

---

## 🧪 Role Molecule Testing

A default Molecule scenario is provided under `molecule/default` and covers:

- Resource creation and update
- Secret management
- Custom Resource deployment
- Proper deletion and cleanup

Run from the role directory:

```bash
cd roles/install_gitlab
molecule test
```

Or individual steps:

```bash
molecule converge
molecule idempotence
molecule verify
molecule destroy
```

Your `molecule.yml` wires `converge`, `verify`, and `destroy` to their respective playbooks.

---

## 📁 Role Structure

```text
install_gitlab/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   ├── argument_specs.yml
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
│   ├── delete-gitlab-operator.yml
│   ├── install-gitlab-operator.yml
│   └── main.yml
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/
    └── main.yml
```
