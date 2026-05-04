# Test Plan — ado.openshift.service_accounts

This doc describes how to validate the role locally and in CI (Molecule).

---

## 0) Prereqs

- OpenShift/Kubernetes cluster reachable.
- `K8S_AUTH_*` exported (or use kubeconfig via module params).
- Collections installed:
  - `ansible-galaxy collection install kubernetes.core`
- Optional CLIs: `oc`, `jq`.

---

## 1) Happy-path — Create (single ns)

### Input
`molecule/default/converge.yml`:

```yaml
- name: Create SAs and bindings
  hosts: localhost
  gather_facts: false
  vars:
    name_space: tools
    service_accounts:
      - { service_account: aap,      state: present, role: cluster-admin, role_kind: ClusterRole, bind_scope: cluster, scc_context: anyuid, token: true }
      - { service_account: cli-tool, state: present, role: cluster-devel, role_kind: ClusterRole, bind_scope: cluster, scc_context: none,   token: false }
  roles:
    - ado.openshift.service_accounts
```

### Verify (CLI)
```bash
# SAs
oc get sa -n tools | grep -E 'aap|cli-tool'

# ClusterRoleBindings
oc get clusterrolebindings | grep -E 'rb-aap-tools-cluster-admin|rb-cli-tool-tools-cluster-devel'

# SCC RoleBinding for anyuid
oc get rolebinding -n tools | grep 'use-anyuid-scc-aap'

# Token Secret exists for aap
oc get secret aap-token -n tools -o jsonpath='{.type}{"\n"}{.metadata.annotations.kubernetes\.io/service-account\.name}{"\n"}'
```

### Verify (facts)
Run with high verbosity or add:

```yaml
- debug: var=sa_tokens
```

Expected:
```yaml
sa_tokens:
  tools:
    aap: eyJhbGciOiJ...
```
No entry for `cli-tool`.

---

## 2) Idempotence

Run:
```bash
molecule idempotence
```
Expected: `Idempotence completed successfully`.

---

## 3) Delete (single ns)

`molecule/default/destroy.yml`:

```yaml
- name: Destroy SAs and bindings
  hosts: localhost
  gather_facts: false
  vars:
    name_space: tools
    service_accounts:
      - { service_account: aap,      state: absent, role: cluster-admin, role_kind: ClusterRole, bind_scope: cluster, scc_context: anyuid }
      - { service_account: cli-tool, state: absent, role: cluster-devel, role_kind: ClusterRole, bind_scope: cluster }
  roles:
    - ado.openshift.service_accounts
```

Run:
```bash
molecule destroy
```

Verify:
```bash
oc get sa -n tools | grep -E 'aap|cli-tool'      # should be empty
oc get clusterrolebindings | grep 'rb-aap-tools-cluster-admin' || echo "gone"
oc get clusterrolebindings | grep 'rb-cli-tool-tools-cluster-devel' || echo "gone"
oc get rolebinding -n tools | grep 'use-anyuid-scc-aap' || echo "gone"
oc get secret aap-token -n tools || echo "gone"
```

---

## 4) All namespaces with excludes (spot check)

Run a create with:
```yaml
name_space: all
exclude_namespaces: [ kube-system, openshift-monitoring, openshift-ingress ]
service_accounts:
  - { service_account: support-bot, state: present, role: view, role_kind: Role, bind_scope: namespace }
```

Verify:
```bash
# spot check a few namespaces (not excluded) have the SA and RB
for ns in $(oc get ns -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'               | grep -v -E 'kube-system|openshift-monitoring|openshift-ingress'); do
  oc get sa -n "$ns" support-bot >/dev/null 2>&1 || echo "missing in $ns"
done
```

---

## 5) Negative cases

- **Invalid role_kind** → expect module failure.
- **SCC that doesn’t exist** → RoleBinding still created, but SCC effect depends on cluster setup.
- **token: true + state: absent** → no token created; token Secret deletion attempted (ok if not found).

---

## 6) Security checks

- Ensure tokens aren’t printed unless you explicitly add a print task.
- Keep `no_log: true` on token-handling tasks; enable temporarily for debugging only.

---

## 7) Naming sanity

Confirm name patterns match create/delete:
- CRB/RB: `rb-<sa>-<ns>-<role-with-colons→dashes>`
- SCC RB: `use-<scc>-scc-<sa>`
- Token Secret: `<sa>-token`

If you fork naming, update both create & delete.

---

## 8) CI hints

- Export kube auth in CI job env (`K8S_AUTH_HOST`, `K8S_AUTH_API_KEY`, `K8S_AUTH_VERIFY_SSL`).
- Run:
  ```bash
  molecule converge
  molecule idempotence
  molecule destroy
  ```
  