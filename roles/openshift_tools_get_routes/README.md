# Role: ado.openshift.get_routes

Read-only role that **retrieves OpenShift Routes** and exposes useful facts.

- Returns: `routes`, `route_hosts`, `primary_route`, `primary_host`
- Never creates or mutates cluster resources (safe to run in CI)
- Works with kubeconfig **or** host+token auth
- **NEW:** Supports querying routes from multiple namespaces with the `multiple_routes` and `routes` options.
  - If `multiple_routes: true` and `routes` list is set, gathers and prints routes from all listed namespaces.
  - If `multiple_routes` is not set or false, runs in single-namespace mode (default).

---

## Requirements

- OpenShift/Kubernetes API access (via kubeconfig or env vars)
- `kubernetes.core` collection installed

---

## Variables

| Variable            | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `name_space`        | Namespace to query. Omit to search all namespaces.                          |
| `multiple_routes`   | If `true`, query all namespaces in `routes` list instead of just one.       |
| `routes`            | List of namespaces to query for routes (used if `multiple_routes: true`).   |
| `validate_certs`    | TLS verification for API calls (`true` with a trusted CA; set `false` for lab/self‑signed). |

### Auth via environment (optional)

| Variable             | Description                                   |
|----------------------|-----------------------------------------------|
| `KUBECONFIG`         | Path to kubeconfig (alternative to host+token). |
| `K8S_AUTH_HOST`      | API server URL, e.g. `https://api.cluster:6443`. |
| `K8S_AUTH_API_KEY`   | Bearer token for the API.                       |
| `K8S_AUTH_VERIFY_SSL`| `true`/`false` TLS verify toggle.               |
| `K8S_AUTH_SSL_CA_CERT`| Path to CA bundle file when verifying TLS.     |

---

## Examples

### Get a specific Route by name
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.get_routes
      vars:
        name_space: my-app
        validate_certs: true
```

### Get routes from multiple namespaces
```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.get_routes
      vars:
        multiple_routes: true
        routes:
          - gitlab
          - rhtk
          - acs
          - postfix
          - devspaces
        validate_certs: true
```

---

## Behavior Notes

- This role is **read-only** and only performs `GET` queries via `kubernetes.core.k8s_info`.
- You must have permission to `get/list` `route.openshift.io/v1` `Route` objects in the target namespace(s).
- Returned facts:
  - `routes`: full list of Route resources (list)
  - `route_hosts`: list of `spec.host` values (list)
  - `primary_route`: first Route object (dict) or `{}`
  - `primary_host`: `spec.host` of the first Route or empty string
  - **When `multiple_routes: true`, outputs a list of routes grouped by namespace.**

---

## Molecule

A default Molecule scenario is included for this role. It:

```
dependency → lint → syntax → create → converge → idempotence → destroy → verify
```

- Uses your **namespace** role to create a temporary test namespace.
- Creates a minimal **Service** and **Route** as fixtures.
- Runs this `get_routes` role to fetch the fixture and prints `primary_host`.
- Finally deletes the namespace (which removes the fixture).

> If your cluster uses a self‑signed cert, either provide a CA file and keep `k8s_validate_certs: true`, or temporarily set `K8S_AUTH_VERIFY_SSL=false` for tests.

---

## Author
- Chad Elliott (<chelliot@redhat.com>) 

---

## Repository layout (role)

```text
roles/
└─ get_routes/
   ├─ README.md                 # ← this file
   ├─ defaults/
   │  └─ main.yml
   ├─ tasks/
   │  ├─ main.yml
   │  └─ get_routes.yml
   ├─ molecule/
   │  └─ default/
   │     ├─ converge.yml
   │     ├─ destroy.yml
   │     ├─ molecule.yml        # includes lint stage
   │     ├─ verify.yml
   │     └─ README.md           # per-scenario guide
   ├─ vars/
   │  └─ main.yml               # (optional)
   ├─ handlers/
   │  └─ main.yml               # (optional)
   ├─ templates/                # (optional)
   └─ files/                    # (optional)
```
