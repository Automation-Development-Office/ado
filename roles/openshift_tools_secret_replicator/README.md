# Role: `infra.ado.openshift_tools_secret_replicator`

An Ansible role that reads a Kubernetes `Secret` once, optionally writes the same payload to HashiCorp Vault KV v2, then replicates the `type` and `data` to other namespaces and/or clusters via `kubernetes.core.k8s`.

## Requirements

- **Ansible**: 2.2 or later per `meta/main.yml`; use an Ansible Core release compatible with the collections below (they typically expect a current Core release).
- **Collections** (see `meta/requirements.yml`):
  - `kubernetes.core` — `kubernetes.core.k8s` / `kubernetes.core.k8s_info`
- `community.hashi_vault` (>= 4.2.0) — `community.hashi_vault.vault_kv2_write` when `openshift_tools_secret_replicator_vault_push` is enabled
- **Python packages**:
  - `kubernetes` — required by `kubernetes.core`
  - `PyYAML`
  - `hvac` — required by `community.hashi_vault` when using Vault
- **Kubernetes access**:
  - Valid kubeconfig with RBAC to read the source secret and create/update secrets in target namespaces and contexts
- **HashiCorp Vault** (only when `openshift_tools_secret_replicator_vault_push: true`):
  - Reachable Vault API; authenticate using module parameters and/or environment (`VAULT_ADDR`, `VAULT_TOKEN`, etc.)

Install collections from this role’s requirements file:

```bash
ansible-galaxy collection install -r meta/requirements.yml
```

Install Python dependencies (adjust for your environment):

```bash
pip install kubernetes pyyaml hvac
```

## Variables

### Replication toggles and source

| Variable | Description |
|----------|-------------|
| `openshift_tools_secret_replicator_cluster_replication` | When `true`, replicate to each entry in `openshift_tools_secret_replicator_target_clusters` using that entry’s kube `context` and `ns`. **Default:** `true`. |
| `openshift_tools_secret_replicator_namespace_replication` | When `true`, replicate to each namespace in `openshift_tools_secret_replicator_target_namespaces` on the default/current cluster context. **Default:** `true`. |
| `openshift_tools_secret_replicator_source_secret_name` | Name of the Kubernetes Secret to read. **Default:** `source-secret-name`. |
| `openshift_tools_secret_replicator_source_namespace` | Namespace containing the source Secret. **Default:** `source-namespace`. |
| `openshift_tools_secret_replicator_target_namespaces` | Namespaces on the active context that receive a copy of the secret (when `openshift_tools_secret_replicator_namespace_replication` is true). **Default:** `dev-app`, `staging-app`, `qa-app`. |
| `openshift_tools_secret_replicator_target_clusters` | Per-cluster targets when `openshift_tools_secret_replicator_cluster_replication` is true. **Default:** see below. |

#### `openshift_tools_secret_replicator_target_clusters` structure

Each item must define:

- `context` — kubeconfig context name
- `ns` — namespace in that cluster

Default:

```yaml
openshift_tools_secret_replicator_target_clusters:
  - { context: 'cluster-east', ns: 'prod' }
  - { context: 'cluster-west', ns: 'prod' }
  - { context: 'cluster-dev',  ns: 'sandbox' }
```

### HashiCorp Vault KV v2 (optional)

When `openshift_tools_secret_replicator_vault_push: true`, the role runs `tasks/hashicorp.yml` immediately after loading the source secret (before namespace and cluster replication). The play registers the result of `vault_kv2_write` and prints a debug message with the Vault response when push is enabled.

| Variable | Default | Description |
|----------|---------|-------------|
| `openshift_tools_secret_replicator_vault_push` | `false` | Enable push of the secret payload to Vault KV v2. |
| `openshift_tools_secret_replicator_vault_url` | `""` | Vault API URL; if empty, the module relies on `VAULT_ADDR` and other usual Vault environment variables. |
| `openshift_tools_secret_replicator_vault_token` | `""` | Token; if empty, omitted so environment-based auth can be used. |
| `openshift_tools_secret_replicator_vault_kv_mount` | `"secret"` | KV v2 secrets engine mount path. |
| `openshift_tools_secret_replicator_vault_kv_path` | `"{{ openshift_tools_secret_replicator_source_namespace }}/{{ openshift_tools_secret_replicator_source_secret_name }}"` | Secret path under the mount (mount name not included). |
| `openshift_tools_secret_replicator_vault_namespace` | `""` | Vault Enterprise namespace (optional); empty omits the parameter. |
| `openshift_tools_secret_replicator_vault_validate_certs` | `true` | TLS validation for Vault API. |
| `openshift_tools_secret_replicator_vault_secret_values_base64` | `false` | If `true`, store the same base64 strings as the Kubernetes API (often better for binary keys); if `false`, values are handled per module defaults. |
| `openshift_tools_secret_replicator_vault_store_k8s_secret_type` | `true` | If `true`, include the Kubernetes secret `type` in the Vault data using `openshift_tools_secret_replicator_vault_k8s_secret_type_key`. |
| `openshift_tools_secret_replicator_vault_k8s_secret_type_key` | `"k8s_secret_type"` | Key name used when `openshift_tools_secret_replicator_vault_store_k8s_secret_type` is true. |

## Dependencies

No other Ansible Galaxy **roles** are required (`dependencies: []` in `meta/main.yml`). Install the **collections** listed under Requirements using `meta/requirements.yml`.

## Examples

### Replicate to multiple namespaces (same cluster)

```yaml
---
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.openshift_tools_secret_replicator
      vars:
        openshift_tools_secret_replicator_source_secret_name: "mysql-credentials"
        openshift_tools_secret_replicator_source_namespace: "production"
        openshift_tools_secret_replicator_target_namespaces:
          - "staging"
          - "development"
          - "testing"
        openshift_tools_secret_replicator_namespace_replication: true
        openshift_tools_secret_replicator_cluster_replication: false
```

### Cross-cluster replication

```yaml
---
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.openshift_tools_secret_replicator
      vars:
        openshift_tools_secret_replicator_source_secret_name: "tls-cert"
        openshift_tools_secret_replicator_source_namespace: "ingress"
        openshift_tools_secret_replicator_target_clusters:
          - { context: 'us-east', ns: 'ingress' }
          - { context: 'us-west', ns: 'ingress' }
          - { context: 'eu-central', ns: 'ingress' }
        openshift_tools_secret_replicator_namespace_replication: false
        openshift_tools_secret_replicator_cluster_replication: true
```

### Namespaces and clusters

```yaml
---
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.openshift_tools_secret_replicator
      vars:
        openshift_tools_secret_replicator_source_secret_name: "api-key"
        openshift_tools_secret_replicator_source_namespace: "core"
        openshift_tools_secret_replicator_target_namespaces:
          - "auth-service"
          - "payment-service"
        openshift_tools_secret_replicator_target_clusters:
          - { context: 'prod-primary', ns: 'core' }
          - { context: 'prod-backup', ns: 'core' }
        openshift_tools_secret_replicator_namespace_replication: true
        openshift_tools_secret_replicator_cluster_replication: true
```

### Optional: push source secret to Vault KV v2

```yaml
---
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.openshift_tools_secret_replicator
      vars:
        openshift_tools_secret_replicator_source_secret_name: "app-credentials"
        openshift_tools_secret_replicator_source_namespace: "platform"
        openshift_tools_secret_replicator_vault_push: true
        openshift_tools_secret_replicator_vault_kv_mount: "secret"
        openshift_tools_secret_replicator_vault_kv_path: "platform/app-credentials"
        # Optional: set explicitly or rely on VAULT_ADDR / VAULT_TOKEN
        # openshift_tools_secret_replicator_vault_url: "https://vault.example.com:8200"
        # openshift_tools_secret_replicator_vault_token: "{{ lookup('env', 'VAULT_TOKEN') }}"
        openshift_tools_secret_replicator_namespace_replication: false
        openshift_tools_secret_replicator_cluster_replication: false
```

## Molecule

This role includes a Molecule scenario at `molecule/default`. `molecule/default/molecule.yml` sets `ANSIBLE_ROLES_PATH` to the parent of the role directory so the play can resolve `infra.ado.openshift_tools_secret_replicator` during local runs.

Configured **scenario test sequence** (what `molecule test` runs for this scenario):

1. `dependency`
2. `create`
3. `converge`
4. `idempotence`
5. `verify`

Note: `lint`, `syntax`, and `destroy` are not in the default `test_sequence`; run them explicitly when you need them.

For a full manual lifecycle (dependency through verify), use this order:

```bash
molecule dependency
molecule lint
molecule syntax
molecule create
molecule converge
molecule idempotence
molecule destroy
molecule verify
```

### Auth via environment

`molecule/default/molecule.yml` passes Kubernetes auth variables through from your shell environment:

- `K8S_AUTH_HOST`
- `K8S_AUTH_API_KEY`
- `K8S_AUTH_VERIFY_SSL`

Example:

```bash
export K8S_AUTH_HOST="https://api.example-cluster:6443"
export K8S_AUTH_API_KEY="<token>"
export K8S_AUTH_VERIFY_SSL="false"
```

The sample `molecule/default/converge.yml` sets `K8S_AUTH_VERIFY_SSL: "no"` on the play environment for local testing; override with your own values or exports as needed.

## Behavior Notes

- The role reads the source Secret once with `kubernetes.core.k8s_info`, then applies the same `type` and `data` to targets (Vault first if enabled, then namespace and/or cluster loops).
- If the source Secret does not exist, the role fails with a clear message.
- **Labels on replicated Secrets**
  - Namespace targets: `replicated-by: secret-replicator`, `source-ns: <openshift_tools_secret_replicator_source_namespace>`.
  - Cluster targets label `source-ns` and `source-cluster` using `openshift_tools_secret_replicator_target_clusters[0].ns` and `openshift_tools_secret_replicator_target_clusters[0].context` for every cluster iteration (see `tasks/main.yml`); adjust `openshift_tools_secret_replicator_target_clusters` order if that metadata must reflect a specific primary cluster.
- **Vault**: With `openshift_tools_secret_replicator_vault_push: true`, the module receives the Kubernetes `data` map plus Vault-specific options (`openshift_tools_secret_replicator_vault_secret_values_base64`, `openshift_tools_secret_replicator_vault_store_k8s_secret_type`, `openshift_tools_secret_replicator_vault_k8s_secret_type_key`). Consult `community.hashi_vault.vault_kv2_write` for encoding and metadata behavior.

### License

This role is licensed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.html) version 3.0 or later (SPDX-License-Identifier: GPL-3.0-or-later). The full license text is in the [`LICENSE`](../../LICENSE) file at the repository root.

## Repository layout

```text
openshift_tools_secret_replicator/
├── defaults/main.yml
├── handlers/main.yml
├── meta/main.yml
├── meta/requirements.yml
├── molecule/default/
│   ├── converge.yml
│   ├── molecule.yml
│   └── verify.yml
├── tasks/
│   ├── main.yml
│   └── hashicorp.yml
├── tests/
│   ├── inventory
│   └── test.yml
├── vars/main.yml
└── README.md
```
