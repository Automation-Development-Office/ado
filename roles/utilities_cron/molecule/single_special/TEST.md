# Molecule Tests — cron (all scenarios)

**Test sequence**

dependency → syntax → create → converge → idempotence → destroy → verify

## What these tests cover

1. **Dependency**
   - Installs role/collection dependencies via `ansible-galaxy`.

2. **Syntax**
   - Runs `ansible-playbook --syntax-check` on scenario playbooks (basic YAML/Jinja sanity).

3. **Create**
   - Prepares the local runner/connection (localhost driver). Ensures the test variables are set.

4. **Converge**
   - Applies the `ado.utilities.cron` role with various job lists and states:
     - `cron_type`: e.g., `special`
     - `cron_state`: e.g., `present`, `absent`
     - Job lists: `cron_yearly_jobs`, `cron_monthly_jobs`, `cron_weekly_jobs`, `cron_daily_jobs`, `cron_hourly_jobs`, `cron_reboot_jobs`, `cron_annual_jobs`
   - Scenarios include:
     - **full_special**: applies all special cron jobs
     - **full_special_removal**: removes all special cron jobs
     - **single_special**: applies a single special cron job
     - **single_special_removal**: removes a single special cron job
     - **verify_docs**: checks documentation and variable structure

5. **Idempotence**
   - Re-runs converge and expects **`changed=0`** (no re-applies).

6. **Destroy**
   - Cleans up cron jobs if removal scenarios are run; otherwise, step is a no-op.

7. **Verify**
   - Asserts cron jobs are present or absent as expected.
   - Checks **README.md** exists and has basic structure (see below).
   - Validates job entries in the crontab.
   - Runs verification playbooks from `cron/tests/`:
     - `verify_full_special.yml`
     - `verify_full_special_removal.yml`
     - `verify_single_special.yml`
     - `verify_single_special_removal.yml`
     - `verify_docs.yml`

## README.md checks (verify step)

The verify play performs:

- ✅ **Existence**: `README.md` must be present at the role root.
- ✅ **Heading**: first heading starts with `# Role:`
  (regex: `(?m)^#\s+Role:`)
- ✅ **Variables table**: contains a header row like `| Variable | Description |`
  (regex: `\|\s*Variable\s*\|\s*Description\s*\|`)
- ✅ **Example code block**: fenced block like `yaml … ` (yaml/yml/ansible/bash)
  (regex: `(yaml|yml|ansible|bash)[\s\S]*?`)

## Python version note

- Managed hosts must have **Python ≥ 3.7**. Python **3.6 and older cannot use `service_facts`**, so the role will no-op (and the scenario marks converge-related checks as **skipped** on those hosts).

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

## Customizing the tested cron jobs

Override via environment or edit `molecule/<scenario>/group_vars/all`:

```yaml
cron_type: special
cron_state: present
cron_yearly_jobs:
  - { name: "yearly_test", job: "test" }
cron_monthly_jobs:
  - { name: "monthly_test", job: "test" }
# ...other job lists...
```

## Linting

- **Ansible syntax** runs automatically in the **`syntax`** step.
- **ansible-lint**: recommended to run locally/CI:
  ```bash
  ansible-lint --offline roles/cron
  ```

# full cycle

molecule test

# or step-by-step

molecule converge
molecule idempotence
molecule destroy
molecule verify

Auth/TLS notes
Provide either:

molecule_root_password: "YOURPASSWORD"

```

```
