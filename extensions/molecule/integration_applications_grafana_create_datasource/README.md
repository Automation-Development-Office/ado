# Molecule scenario: integration_applications_grafana_create_datasource

This scenario validates wiring for the
`infra.ado.applications_grafana_create_datasource` role in the normalized
extension-level Molecule layout.

## Scenario flow

1. `prepare`
2. `converge`
3. `idempotence`
4. `verify`
5. `destroy` (via `destroy_sequence`)

## Playbook mapping

Scenario `molecule.yml` points to shared playbooks in
`extensions/molecule/utils/playbooks`:

- `prepare`: `applications_grafana_create_datasource_prepare.yml`
- `converge`: `applications_grafana_create_datasource_converge.yml`
- `verify`: `applications_grafana_create_datasource_verify.yml`
- `destroy`: `applications_grafana_create_datasource_destroy.yml`

## Run

From `extensions/molecule`:

```bash
molecule test -s integration_applications_grafana_create_datasource
```

## Live-check mode

Converge is safe by default and skips live external calls unless explicitly
enabled. To run the role against real OpenShift/Grafana endpoints:

```bash
export APPLICATIONS_GRAFANA_CREATE_DATASOURCE_ENABLE_LIVE_CHECKS=true
export APPLICATIONS_GRAFANA_CREATE_DATASOURCE_HOSTNAME="grafana.example.com"
export APPLICATIONS_GRAFANA_CREATE_DATASOURCE_ADMIN_USER="admin"
export APPLICATIONS_GRAFANA_CREATE_DATASOURCE_ADMIN_PASSWORD="***"
molecule test -s integration_applications_grafana_create_datasource
```
