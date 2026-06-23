# Molecule Tests — wait_for_pods_running (default scenario)

**Test sequence**

dependency → syntax → create → converge → idempotence → destroy → verify

## What these tests cover

1. **Dependency**
   - Installs role/collection deps via `ansible-galaxy`.

2. **Syntax**
   - Runs `ansible-playbook --syntax-check` on scenario playbooks (basic YAML/Jinja sanity).

3. **Create**
   - Prepares the local runner/connection (localhost driver).

4. **Converge**
   - Ensures a test namespace exists via the `namespace` role:
     - `name_space: test-wait-pods-molecule`
   - Creates a small Deployment in that namespace:
     - name: `hello`, replicas: `2`, label: `app=hello`
   - Applies the `wait_for_pods_running` role with:
     - `name_space: test-wait-pods-molecule`
     - `label_selector: app=hello`
     - `expected_pods: 2`
     - `timeout: 300`
     - `validate_certs: false` (flip to `true` when using a trusted CA)
   - Expects the two pods to reach **Running/Ready**.

5. **Idempotence**
   - Re-runs converge and expects **`changed=0`** (no re-applies).
     _If your `wait_for_pods_running` role marks tasks as changed on success, consider adjusting the role or skip tags for this stage._

6. **Destroy**
   - Removes the test namespace (or skips if already gone).

7. **Verify**
   - Confirms the namespace is **absent** (cleanup successful).
   - Checks **README.md** exists and has basic structure (see below).

## README.md checks (verify step)

The verify play performs:

- ✅ **Existence**: `README.md` must be present at the role root.
- ✅ **Heading**: first heading starts with `# Role:`
  (regex: `(?m)^#\s+Role:`)
- ✅ **Variables table**: contains a header row like `| Variable | Description |`
  (regex: `\|\s*Variable\s*\|\s*Description\s*\|`)
- ✅ **Example code block**: fenced block like `yaml … ` (yaml/yml/ansible/bash)
  (regex: `(yaml|yml|ansible|bash)[\s\S]*?`)

> These are implemented via `slurp` → `set_fact` → `assert` in `verify.yml`.

## Linting

- **Ansible syntax** runs automatically in the **`syntax`** step.
- **ansible-lint**: recommended to run locally/CI:
  ```bash
  ansible-lint --offline roles/wait_for_pods_running
  ```

## How to run

```bash
# full cycle
molecule test

# or step-by-step
molecule converge
molecule idempotence
molecule destroy
molecule verify
```

## Auth/TLS notes

Provide either:

- **KUBECONFIG** to a valid kubeconfig, **or**
- **K8S_AUTH_HOST + K8S_AUTH_API_KEY**, plus TLS choice:
  - lab: `K8S_AUTH_VERIFY_SSL=false`
  - proper CA: `K8S_AUTH_VERIFY_SSL=true` and `K8S_AUTH_SSL_CA_CERT=/path/to/ca.crt`
