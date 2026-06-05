# Test Notes: integration_jira

This scenario is normalized to the extension-level format used by other
`extensions/molecule/integration_*` scenarios.

## Sequence

```text
prepare -> converge -> idempotence -> verify
```

Destroy sequence:

```text
destroy
```

## Playbook mapping

- `prepare` -> `../utils/playbooks/jira_prepare.yml`
- `converge` -> `../utils/playbooks/jira_converge.yml`
- `verify` -> `../utils/playbooks/jira_verify.yml`
- `destroy` -> `../utils/playbooks/jira_destroy.yml`

## Run

From `extensions/molecule/`:

```bash
molecule test -s integration_jira
```
