# Role: ado.openshift.subscription_operator

Create, update, or remove an **OLM Subscription** for an Operator in OpenShift.  I.E  install a operator

- Installs an Operator by creating a `Subscription`
- Uninstalls by deleting the `Subscription` (and optionally CSV via OLM)
- Works with kubeconfig **or** host+token auth
- **Important:** Your OperatorGroup **must** match the operator’s supported `installModes`

---

## Requirements

- OpenShift/Kubernetes API access (via kubeconfig or env vars)
- `kubernetes.core` collection installed
- A compatible **OperatorGroup** in the target namespace (single-namespace or all-namespaces).  
  _Tip:_ Use your `ado.openshift.operatorgroup` role to create it appropriately.

---

## Variables

| Variable | Description |
|---------|-------------|
| `name_space` | Namespace for the `Subscription`. For AllNamespaces installs, this is typically `openshift-operators`. **Required.** |
| `operator_name` | Operator package name (e.g., `web-terminal`, `advanced-cluster-management`). **Required.** |
| `operator_channel` | Channel to track (e.g., `stable`, `fast`, `release-2.13`). |
| `operator_source` | Catalog source (e.g., `redhat-operators`). |
| `operator_approval` | Install plan approval: `Automatic` (default) or `Manual` (if supported). |
| `state` | `present` to install/ensure, `absent` to uninstall. Default: `present`. |
| `validate_certs` | TLS verification for API calls (`true` with a trusted CA; set `false` in lab/self-signed). |

### Auth via environment (optional)

| Variable | Description |
|---------|-------------|
| `KUBECONFIG` | Path to kubeconfig (alternative to host+token). |
| `K8S_AUTH_HOST` | API server URL, e.g. `https://api.cluster:6443`. |
| `K8S_AUTH_API_KEY` | Bearer token for the API. |
| `K8S_AUTH_VERIFY_SSL` | `true`/`false` TLS verify toggle. |
| `K8S_AUTH_SSL_CA_CERT` | Path to CA bundle when verifying TLS. |

---

## Examples

### Install **Web Terminal** operator (AllNamespaces) in `openshift-operators`
> Web Terminal supports **AllNamespaces** only; install into `openshift-operators` and use an AllNamespaces OperatorGroup.

```yaml
- hosts: localhost
  gather_facts: false
  pre_tasks:
    - name: Ensure global OperatorGroup (AllNamespaces)
      ansible.builtin.include_role:
        name: ado.openshift.operatorgroup
      vars:
        state: present
        all_namespaces_install: true
        validate_certs: true

  roles:
    - role: ado.openshift.subscription_operator
      vars:
        name_space: openshift-operators
        operator_name: web-terminal
        operator_channel: fast          # or stable (check your catalog)
        operator_source: redhat-operators
        operator_approval: Automatic
        state: present
        validate_certs: true
```

### Install a **SingleNamespace** operator into an app namespace
> Use only if the operator’s CSV supports `SingleNamespace`. Ensure a single-ns OperatorGroup exists first.

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.subscription_operator
      vars:
        name_space: my-app
        operator_name: devworkspace-operator
        operator_channel: stable
        operator_source: redhat-operators
        operator_source_namespace: openshift-marketplace
        state: present
        validate_certs: true
```

### Uninstall an operator (delete the Subscription)
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.subscription_operator
      vars:
        name_space: openshift-operators
        operator_name: web-terminal
        state: absent
        validate_certs: true
```

---

## Behavior Notes

- **OperatorGroup vs installModes**: The Operator’s CSV defines supported modes. The OG must match:
  - **AllNamespaces** → install Subscription in `openshift-operators` with **no** `targetNamespaces`.
  - **SingleNamespace** → install in your app namespace with OG `spec.targetNamespaces: [ name_space ]`.
- **How to check channels/installModes**:
  ```bash
  oc -n openshift-marketplace get packagemanifest <operator_name> -o jsonpath='{.status.channels[*].name}'
  oc -n openshift-marketplace get packagemanifest <operator_name> -o jsonpath='{.status.channels[?(@.name=="<channel>")].currentCSVDesc.installModes}'
  ```
- The role focuses on the `Subscription`. OLM creates the `InstallPlan` and `ClusterServiceVersion`.
- On `state: absent`, OLM will remove the Subscription; CSV removal timing may vary (finalizers/usage).

---

## Molecule

A default Molecule scenario is provided (see `molecule/default`). It installs **Web Terminal** in `openshift-operators` using an **AllNamespaces** OG, waits for CSV `phase=Succeeded`, and then uninstalls during destroy.

```
dependency → lint → syntax → create → converge → idempotence → destroy → verify
```

> If your catalog differs, override `operator_name`, `operator_channel`, and/or namespace.

---

## Author
- Chad Elliott (<chelliot@redhat.com>) 

---

## Repository layout (role)

```text
roles/
└─ subscription_operator/
   ├─ README.md                 # ← this file
   ├─ defaults/
   │  └─ main.yml
   ├─ tasks/
   │  ├─ main.yml
   │  └─ install_operator.yml
   ├─ molecule/
   │  └─ default/
   │     ├─ converge.yml
   │     ├─ destroy.yml
   │     ├─ molecule.yml
   │     ├─ verify.yml
   │     ├─ README.md
   │     └─ TEST.md
   ├─ vars/
   │  └─ main.yml
   ├─ handlers/
   │  └─ main.yml               # (optional)
   └─ tests/
      └─ inventory
```