# Molecule Tests — lookup_operator_defaults (default scenario)

**Test sequence**

dependency → syntax → create → converge → idempotence → verify

## What these tests cover

1. **Dependency**
   - Installs role/collection deps via `ansible-galaxy`.

2. **Syntax**
   - Runs `ansible-playbook --syntax-check` on scenario playbooks (basic YAML/Jinja sanity).

3. **Create**
   - Prepares the local runner/connection (localhost driver).

4. **Converge**
   - Applies the `lookup_operator_defaults` role with:
     - `app_name: web-terminal` (example; override as needed)
   - Expects the play to complete without error and to set a fact named `operator_defaults` (dict).

5. **Idempotence**
   - Re-runs converge and expects **`changed=0`** (pure lookup should not report changes).

6. **Verify**
   - Asserts that:
     - The `operator_defaults` fact exists and is a dictionary.
     - (Optionally) required keys exist — update `verify.yml` to match your schema (e.g., `operator_name`, `operator_channel`, `operator_source`, `operator_source_namespace`).
   - Checks **README.md** exists and has basic structure:
     - ✅ **Heading**: starts with `# Role:`  (regex: `(?m)^#\s+Role:`)
     - ✅ **Variables table**: contains header `| Variable | Description |`  (regex: `\|\s*Variable\s*\|\s*Description\s*\|`)
     - ✅ **Example code block**: fenced block like ```yaml … ``` (yaml/yml/ansible/bash)  (regex: ```(yaml|yml|ansible|bash)[\s\S]*?```)

> These README checks are implemented via `slurp` → `set_fact` → `assert` in `verify.yml`.

## How to run

```bash
# full cycle
molecule test

# or step-by-step
molecule converge
molecule idempotence
molecule verify
```

## Notes
- If your role uses a different fact name than `operator_defaults`, update the verify assertions accordingly.
- Because this role is read-only, there is **no destroy step** in this scenario.

## Linting
- **Ansible syntax** runs automatically in the **`syntax`** step.
- **ansible-lint**: recommended to run locally/CI:
  ```bash
  ansible-lint --offline roles/namespace


# full cycle
molecule test

# or step-by-step
molecule converge
molecule idempotence
molecule destroy
molecule verify

Auth/TLS notes
Provide either:

KUBECONFIG to a valid kubeconfig, or

K8S_AUTH_HOST + K8S_AUTH_API_KEY, plus TLS choice:

lab: K8S_AUTH_VERIFY_SSL=false

proper CA: K8S_AUTH_VERIFY_SSL=true and K8S_AUTH_SSL_CA_CERT=/path/to/ca.crt
