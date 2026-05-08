# Role: `infra.ado.openshift_tools_secret_replicator`

An Ansible role that reads a Kubernetes `Secret` once, optionally writes the same payload to HashiCorp Vault KV v2, then replicates the `type` and `data` to other namespaces and/or clusters via `kubernetes.core.k8s`.

## Requirements

- **Ansible**: 2.2 or later per `meta/main.yml`; use an Ansible Core release compatible with the collections below (they typically expect a current Core release).
- **Collections** (see `meta/requirements.yml`):
  - `kubernetes.core` — `kubernetes.core.k8s` / `kubernetes.core.k8s_info`
  - `community.hashi_vault` (>= 4.2.0) — `community.hashi_vault.vault_kv2_write` when `vault_push` is enabled
- **Python packages**:
  - `kubernetes` — required by `kubernetes.core`
  - `PyYAML`
  - `hvac` — required by `community.hashi_vault` when using Vault
- **Kubernetes access**:
  - Valid kubeconfig with RBAC to read the source secret and create/update secrets in target namespaces and contexts
- **HashiCorp Vault** (only when `vault_push: true`):
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
| `cluster_replication` | When `true`, replicate to each entry in `target_clusters` using that entry’s kube `context` and `ns`. **Default:** `true`. |
| `namespace_replication` | When `true`, replicate to each namespace in `target_namespaces` on the default/current cluster context. **Default:** `true`. |
| `source_secret_name` | Name of the Kubernetes Secret to read. **Default:** `source-secret-name`. |
| `source_namespace` | Namespace containing the source Secret. **Default:** `source-namespace`. |
| `target_namespaces` | Namespaces on the active context that receive a copy of the secret (when `namespace_replication` is true). **Default:** `dev-app`, `staging-app`, `qa-app`. |
| `target_clusters` | Per-cluster targets when `cluster_replication` is true. **Default:** see below. |

#### `target_clusters` structure

Each item must define:

- `context` — kubeconfig context name
- `ns` — namespace in that cluster

Default:

```yaml
target_clusters:
  - { context: 'cluster-east', ns: 'prod' }
  - { context: 'cluster-west', ns: 'prod' }
  - { context: 'cluster-dev',  ns: 'sandbox' }
```

### HashiCorp Vault KV v2 (optional)

When `vault_push: true`, the role runs `tasks/vault.yml` immediately after loading the source secret (before namespace and cluster replication). The play registers the result of `vault_kv2_write` and prints a debug message with the Vault response when push is enabled.

| Variable | Default | Description |
|----------|---------|-------------|
| `vault_push` | `false` | Enable push of the secret payload to Vault KV v2. |
| `vault_url` | `""` | Vault API URL; if empty, the module relies on `VAULT_ADDR` and other usual Vault environment variables. |
| `vault_token` | `""` | Token; if empty, omitted so environment-based auth can be used. |
| `vault_kv_mount` | `"secret"` | KV v2 secrets engine mount path. |
| `vault_kv_path` | `"{{ source_namespace }}/{{ source_secret_name }}"` | Secret path under the mount (mount name not included). |
| `vault_namespace` | `""` | Vault Enterprise namespace (optional); empty omits the parameter. |
| `vault_validate_certs` | `true` | TLS validation for Vault API. |
| `vault_secret_values_base64` | `false` | If `true`, store the same base64 strings as the Kubernetes API (often better for binary keys); if `false`, values are handled per module defaults. |
| `vault_store_k8s_secret_type` | `true` | If `true`, include the Kubernetes secret `type` in the Vault data using `k8s_secret_type_key`. |
| `vault_k8s_secret_type_key` | `"k8s_secret_type"` | Key name used when `vault_store_k8s_secret_type` is true. |

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
        source_secret_name: "mysql-credentials"
        source_namespace: "production"
        target_namespaces:
          - "staging"
          - "development"
          - "testing"
        namespace_replication: true
        cluster_replication: false
```

### Cross-cluster replication

```yaml
---
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.openshift_tools_secret_replicator
      vars:
        source_secret_name: "tls-cert"
        source_namespace: "ingress"
        target_clusters:
          - { context: 'us-east', ns: 'ingress' }
          - { context: 'us-west', ns: 'ingress' }
          - { context: 'eu-central', ns: 'ingress' }
        namespace_replication: false
        cluster_replication: true
```

### Namespaces and clusters

```yaml
---
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.openshift_tools_secret_replicator
      vars:
        source_secret_name: "api-key"
        source_namespace: "core"
        target_namespaces:
          - "auth-service"
          - "payment-service"
        target_clusters:
          - { context: 'prod-primary', ns: 'core' }
          - { context: 'prod-backup', ns: 'core' }
        namespace_replication: true
        cluster_replication: true
```

### Optional: push source secret to Vault KV v2

```yaml
---
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.openshift_tools_secret_replicator
      vars:
        source_secret_name: "app-credentials"
        source_namespace: "platform"
        vault_push: true
        vault_kv_mount: "secret"
        vault_kv_path: "platform/app-credentials"
        # Optional: set explicitly or rely on VAULT_ADDR / VAULT_TOKEN
        # vault_url: "https://vault.example.com:8200"
        # vault_token: "{{ lookup('env', 'VAULT_TOKEN') }}"
        namespace_replication: false
        cluster_replication: false
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
  - Namespace targets: `replicated-by: secret-replicator`, `source-ns: <source_namespace>`.
  - Cluster targets label `source-ns` and `source-cluster` using `target_clusters[0].ns` and `target_clusters[0].context` for every cluster iteration (see `tasks/main.yml`); adjust `target_clusters` order if that metadata must reflect a specific primary cluster.
- **Vault**: With `vault_push: true`, the module receives the Kubernetes `data` map plus Vault-specific options (`secret_values_base64`, `store_k8s_secret_type`, `k8s_secret_type_key`). Consult `community.hashi_vault.vault_kv2_write` for encoding and metadata behavior.

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
│   └── vault.yml
├── tests/
│   ├── inventory
│   └── test.yml
├── vars/main.yml
└── README.md
```
