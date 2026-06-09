# Integration Scenario: jira

This directory defines the extension-level Molecule scenario
`integration_jira`.

The scenario follows the shared `extensions/molecule` pattern and points to
utility playbooks under `extensions/molecule/utils/playbooks/`.

## Referenced playbooks

- `jira_prepare.yml`
- `jira_converge.yml`
- `jira_verify.yml`
- `jira_destroy.yml`

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
molecule test -s integration_jira
```
