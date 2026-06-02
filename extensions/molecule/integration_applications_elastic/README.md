# Molecule scenario: integration_applications_elastic

This scenario validates the `infra.ado.applications_elastic` role using the
normalized extension-level Molecule layout.

## Scenario flow

1. `prepare`
2. `converge`
3. `idempotence`
4. `verify`
5. `destroy` (via `destroy_sequence`)

## Playbook mapping

The scenario-level `molecule.yml` maps to shared playbooks under
`extensions/molecule/utils/playbooks`:

- `prepare`: `applications_elastic_prepare.yml`
- `converge`: `applications_elastic_converge.yml`
- `verify`: `applications_elastic_verify.yml`
- `destroy`: `applications_elastic_destroy.yml`

## Run

From `extensions/molecule`:

```bash
molecule test -s integration_applications_elastic
```

## Live-check mode

Converge is safe by default and skips live endpoint checks unless explicitly enabled.
To run role status checks against a real Elasticsearch endpoint:

```bash
export APPLICATIONS_ELASTIC_ENABLE_LIVE_CHECKS=true
export APPLICATIONS_ELASTIC_URL="http://localhost:9200"
molecule test -s integration_applications_elastic
```
