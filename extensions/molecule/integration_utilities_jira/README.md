# Integration Scenario: utilities_jira

This directory defines the extension-level Molecule scenario
`integration_utilities_jira`.

The scenario follows the shared `extensions/molecule` pattern and points to
utility playbooks under `extensions/molecule/utils/playbooks/`.

## Referenced playbooks

- `utilities_jira_prepare.yml`
- `utilities_jira_converge.yml`
- `utilities_jira_verify.yml`
- `utilities_jira_destroy.yml`

## Test sequence

```text
prepare -> converge -> idempotence -> verify
```

Destroy sequence:

```text
destroy
```

## Run locally

From `extensions/molecule/`:

```bash
molecule test -s integration_utilities_jira
```
