# Molecule scenario: integration_grafana_manage_folders

This scenario validates wiring for the `infra.ado.grafana_manage_folders`
role in the normalized extension-level Molecule layout.

## Scenario flow

1. `prepare`
2. `converge`
3. `idempotence`
4. `verify`
5. `destroy` (via `destroy_sequence`)

## Playbook mapping

Scenario `molecule.yml` points to shared playbooks in
`extensions/molecule/utils/playbooks`:

- `prepare`: `grafana_manage_folders_prepare.yml`
- `converge`: `grafana_manage_folders_converge.yml`
- `verify`: `grafana_manage_folders_verify.yml`
- `destroy`: `grafana_manage_folders_destroy.yml`

## Run

From `extensions/molecule`:

```bash
molecule test -s integration_grafana_manage_folders
```

## Live-check mode

Converge is safe by default and skips live external calls unless explicitly
enabled. To run the role against a real Grafana endpoint:

```bash
export GRAFANA_MANAGE_FOLDERS_ENABLE_LIVE_CHECKS=true
export GRAFANA_MANAGE_FOLDERS_NAME="General"
export GRAFANA_MANAGE_FOLDERS_HOSTNAME="grafana.example.com"
export GRAFANA_MANAGE_FOLDERS_ADMIN_USER="admin"
export GRAFANA_MANAGE_FOLDERS_ADMIN_PASSWORD="***"
molecule test -s integration_grafana_manage_folders
```
