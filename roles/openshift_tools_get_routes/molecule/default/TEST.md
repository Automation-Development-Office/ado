---

### `TEST.md`

```markdown
# Molecule Tests — get_routes (default scenario)

**Test sequence**

dependency → lint → syntax → create → converge → idempotence → destroy → verify

## What these tests cover

1. **Dependency**
   - Installs required collections (e.g., `kubernetes.core`) via `ansible-galaxy`.

2. **Lint**
   - Runs `ansible-lint` over this role directory (`--offline`). Uses the repo’s root `.ansible-lint` if present.

3. **Syntax**
   - `ansible-playbook --syntax-check` on scenario playbooks.

4. **Create**
   - Local driver bootstrap (localhost).

5. **Converge**
   - Calls `ado.openshift.namespace` (`state: present`) to create `test-routes-molecule`.
   - Creates a minimal `Service` (`echo-svc`) and `Route` (`echo`) as test fixtures.
   - Runs the **read-only** `ado.openshift.get_routes` role with:
     - `route_namespace: test-routes-molecule`
     - `route_name: echo`
     - `require_found: true`
   - Exposes facts:
     - `routes` (list), `route_hosts` (list of hosts), `primary_route` (first item), `primary_host` (first host).

6. **Idempotence**
   - Re-runs converge; expects **`changed=0`**.

7. **Destroy**
   - Calls `ado.openshift.namespace` (`state: absent`) to delete the namespace (which removes the route & service).

8. **Verify**
   - Validates **README.md** exists and has a basic structure (see below).

---

## README.md checks (verify step)

The verify play performs:

- ✅ **Existence**: `README.md` present at the role root.
- ✅ **Heading**: first heading starts with `# Role:`  
  (regex: `(?m)^#\s+Role:`)
- ✅ **Variables table**: includes `| Variable | Description |`  
  (regex: `\|\s*Variable\s*\|\s*Description\s*\|`)
- ✅ **Example code block**: fenced block like ```yaml … ``` (yaml/yml/ansible/bash)  
  (regex: ```(yaml|yml|ansible|bash)[\s\S]*?```)

(Implemented via `slurp` → `set_fact` → `assert` in `verify.yml`.)

---

## Linting

- Molecule runs `ansible-lint` during the **`lint`** stage thanks to the scenario’s `lint:` block.
- Run directly if needed:
  ```bash
  ansible-lint --offline roles/get_routes

Auth/TLS notes
Provide either:

KUBECONFIG to a valid kubeconfig, or

K8S_AUTH_HOST + K8S_AUTH_API_KEY, plus TLS choice:

lab: K8S_AUTH_VERIFY_SSL=false

proper CA: K8S_AUTH_VERIFY_SSL=true and K8S_AUTH_SSL_CA_CERT=/path/to/ca.crt
