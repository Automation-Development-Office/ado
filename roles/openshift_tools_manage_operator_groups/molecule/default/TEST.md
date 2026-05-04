# Molecule Tests — subscription_operator (default scenario)

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
   - Ensures an **AllNamespaces** OperatorGroup exists in `openshift-operators`.
   - Applies the `subscription_operator` role with:
     - `name_space: openshift-operators`
     - `operator_name: web-terminal`
     - `operator_channel: fast` (override if needed)
     - `operator_source: redhat-operators`
     - `operator_source_namespace: openshift-marketplace`
   - Waits for the Subscription to publish `status.installedCSV`, then waits for the CSV `status.phase == Succeeded`.

5. **Idempotence**
   - Re-runs converge and expects **`changed=0`** (no re-applies).

6. **Destroy**
   - Uninstalls the Subscription (deletes the operator subscription).

7. **Verify**
   - Confirms the Subscription is **absent**.
   - Checks **README.md** exists and has basic structure (see below).


## README.md checks (verify step)
The verify play performs:

- ✅ **Existence**: `README.md` must be present at the role root.
- ✅ **Heading**: first heading starts with `# Role:`  
  (regex: `(?m)^#\s+Role:`)
- ✅ **Variables table**: contains a header row like `| Variable | Description |`  
  (regex: `\|\s*Variable\s*\|\s*Description\s*\|`)
- ✅ **Example code block**: fenced block like ```yaml … ``` (yaml/yml/ansible/bash)  
  (regex: ```(yaml|yml|ansible|bash)[\s\S]*?```)

> These are implemented via `slurp` → `set_fact` → `assert` in `verify.yml`.


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