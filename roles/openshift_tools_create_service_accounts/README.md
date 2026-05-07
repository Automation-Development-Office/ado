
#  Role: ado.openshift.service_accounts

Create, update, or delete Kubernetes/OpenShift **ServiceAccounts** along with:
- RBAC bindings (ClusterRoleBinding or RoleBinding, per item)
- Optional **SCC** grants (via RoleBindings to `system:openshift:scc:<name>`)
- Optional **service account token** creation & collection

Per-item `state` is supported (`present`/`absent`). You can target a single namespace or all namespaces (with optional excludes).

---

## Requirements

- OpenShift/Kubernetes API reachable with auth (via `K8S_AUTH_*` env or module params)
- Collections:
  - `kubernetes.core`
- Tools (for examples/tests): `oc`, `jq` (optional)

---

## Variables

### Top-level

| Variable              | Description |
|----------------------|-------------|
| `name_space`         | Namespace to operate in. Use `'all'` to operate in all namespaces. |
| `exclude_namespaces` | When `name_space: all`, these namespaces are skipped. |
| `service_accounts`   | List of items (see schema below). |

### `service_accounts` item schema

| Key               | Type        | Default      | Meaning |
|-------------------|-------------|--------------|---------|
| `service_account` | string      | **required** | ServiceAccount name. |
| `state`           | string      | `present`    | `present` or `absent` (per-item). |
| `role`            | string      | _empty_      | Name of Role/ClusterRole to bind. Optional. |
| `role_kind`       | string      | `ClusterRole`| `ClusterRole` or `Role`. |
| `bind_scope`      | string      | Auto         | `cluster` if `role_kind: ClusterRole`, else `namespace`. Override if needed. |
| `scc_context`     | string      | _empty_      | Single SCC name, e.g. `anyuid`. Ignored if `'none'`. |
| `scc_contexts`    | list<string>| `[]`         | Additional SCCs to grant. |
| `css_context`     | string      | _empty_      | Back-compat alias for `scc_context`. |
| `token`           | bool        | `false`      | If `true` **and** `state: present`: create a manually-linked token Secret and expose its bearer token as a fact. |

> **Notes**
> - SCCs are granted by creating a **RoleBinding** to the ClusterRole `system:openshift:scc:<scc>`.
> - Token creation uses a Secret of type `kubernetes.io/service-account-token` with annotation `kubernetes.io/service-account.name: <sa>`.
> - Tokens for items with `token: true` are collected into the host fact `sa_tokens`:
>   ```yaml
>   sa_tokens:
>     <namespace>:
>       <service_account>: <bearer-token>
>   ```

---

## Examples

### Minimal (single namespace)

```yaml
- hosts: localhost
  gather_facts: false
  vars:
    name_space: tools
    service_accounts:
      - { service_account: aap, state: present }
  roles:
    - ado.openshift.service_accounts
```

### Create two SAs, cluster-admin for one, scoped role for another, SCC + token

```yaml
- hosts: localhost
  gather_facts: false
  vars:
    name_space: tools
    service_accounts:
      - { service_account: aap,      state: present, role: cluster-admin, role_kind: ClusterRole, bind_scope: cluster, scc_context: anyuid, token: true }
      - { service_account: cli-tool, state: present, role: view,          role_kind: Role,         bind_scope: namespace, scc_context: none,   token: false }
  roles:
    - ado.openshift.service_accounts

# Optional: print the tokens collected for items where token: true
- hosts: localhost
  gather_facts: false
  tasks:
    - name: Show tokens for items that requested token: true
      when: sa_tokens | default({}) | length > 0
      vars:
        _allow: "{{ service_accounts | selectattr('token','equalto', true) | map(attribute='service_account') | list }}"
        _lines: |-
          {% for ns, sdict in sa_tokens.items() -%}
          {% for sa, tok in sdict.items() if sa in _allow -%}
          {{ ns }}/{{ sa }}: {{ tok }}
          {% endfor -%}
          {% endfor -%}
      debug:
        msg: "{{ _lines }}"
```

### All namespaces with excludes

```yaml
- hosts: localhost
  gather_facts: false
  vars:
    name_space: all
    exclude_namespaces:
      - kube-system
      - openshift-monitoring
    service_accounts:
      - { service_account: support-bot, state: present, role: view, role_kind: Role, bind_scope: namespace }
  roles:
    - ado.openshift.service_accounts
```

### Delete (absent)

```yaml
- hosts: localhost
  gather_facts: false
  vars:
    name_space: tools
    service_accounts:
      - { service_account: aap,      state: absent, role: cluster-admin, role_kind: ClusterRole, bind_scope: cluster, scc_context: anyuid }
      - { service_account: cli-tool, state: absent, role: cluster-devel, role_kind: ClusterRole, bind_scope: cluster }
  roles:
    - ado.openshift.service_accounts
```

---

## Outputs

- Host fact `sa_tokens` containing the bearer tokens for all `(namespace, service_account)` that had `token: true` and `state: present`.
- (Optional) You can publish them to AAP/Ansible Controller as a job artifact by adding:
  ```yaml
  - name: Publish service account tokens as artifact
    when: sa_tokens | default({}) | length > 0
    set_stats:
      data:
        service_account_tokens: "{{ sa_tokens }}"
      per_host: false
  ```

> **Security**: tokens are secrets. Avoid printing them in logs unless you explicitly intend to.

## Behavior Notes

- **ServiceAccount**: `<namespace>/sa/<service_account>`
- **ClusterRoleBinding** (cluster scope):  
  `rb-<service_account>-<namespace>-<role-with-colons-replaced-by-dashes>`
- **RoleBinding** (namespace scope):  
  same pattern as above, in the namespace
- **SCC RoleBinding** (namespace scope):  
  `use-<scc>-scc-<service_account>` in the namespace
- **Token Secret** (optional):  
  `<service_account>-token` in the namespace

These are mirrored during deletion.
---

## Idempotency

- The role is idempotent: re-running with the same inputs results in no changes.
- Deletion path removes created bindings, SCC grants, token Secret, and the ServiceAccount.

---

## Troubleshooting

- If you see evaluation errors around `state`/`when`, ensure the role uses **`include_tasks`** (not `import_tasks`) for per-item files so Jinja evaluates at runtime with the current `sa`.
- If printing shows tokens for SAs with `token: false`, you likely have stale `sa_tokens` facts from a previous run. Reset at play start:
  ```yaml
  - set_fact: { sa_tokens: {} }
  ```

---

## Molecule

A default Molecule scenario is included and focuses on ordering + idempotence:

```
dependency → lint → syntax → create → converge → idempotence → destroy → verify
```


A minimal scenario is provided. Set kube auth via env:

```bash
export K8S_AUTH_HOST="https://api.ocp.example:6443"
export K8S_AUTH_API_KEY="…"
export K8S_AUTH_VERIFY_SSL="no"
```

Run:

```bash
molecule converge
molecule idempotence
molecule destroy
```

Your `molecule.yml` wires:
- `converge: molecule/default/converge.yml` (create path)
- `destroy:  molecule/default/destroy.yml` (delete path)

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
│   ├── create_service_account.yml
│   ├── delete_service_account.yml
│   └── main.yml
├── tests
│   ├── inventory
│   └── test.yml
```
