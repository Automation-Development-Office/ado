# Molecule scenario: integration_applications_grafana_manage_folder

This scenario validates wiring for the `infra.ado.applications_grafana_manage_folder`
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

- `prepare`: `applications_grafana_manage_folder_prepare.yml`
- `converge`: `applications_grafana_manage_folder_converge.yml`
- `verify`: `applications_grafana_manage_folder_verify.yml`
- `destroy`: `applications_grafana_manage_folder_destroy.yml`

## Run

From `extensions/molecule`:

```bash
molecule test -s integration_applications_grafana_manage_folder
```

## Live-check mode

Converge is safe by default and skips live external calls unless explicitly
enabled. To run the role against a real Grafana endpoint:

```bash
export APPLICATIONS_GRAFANA_MANAGE_FOLDER_ENABLE_LIVE_CHECKS=true
export APPLICATIONS_GRAFANA_MANAGE_FOLDER_NAME="General"
export APPLICATIONS_GRAFANA_MANAGE_FOLDER_HOSTNAME="grafana.example.com"
export APPLICATIONS_GRAFANA_MANAGE_FOLDER_ADMIN_USER="admin"
export APPLICATIONS_GRAFANA_MANAGE_FOLDER_ADMIN_PASSWORD="***"
molecule test -s integration_applications_grafana_manage_folder
```
