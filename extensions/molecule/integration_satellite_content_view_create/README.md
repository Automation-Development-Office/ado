# Molecule scenario: integration_satellite_content_view_create

This scenario validates the `infra.ado.satellite_content_view` role **create**
action using the extension-level Molecule layout.

## Scenario flow

CI runs the `verify` stage to validate the role README and layout. Full
Satellite integration (prepare, converge, idempotence, destroy) requires
`SATELLITE_*` environment variables.

1. `verify` (default CI sequence)
2. `destroy` (via `destroy_sequence`, removes the test Content View when credentials are set)

## Playbook mapping

The scenario-level `molecule.yml` maps to shared playbooks under
`extensions/molecule/utils/playbooks`:

- `prepare`: `satellite_content_view_prepare_create.yml`
- `converge`: `satellite_content_view_converge_create.yml`
- `verify`: `satellite_content_view_verify.yml`
- `destroy`: `satellite_content_view_destroy_create.yml`

## Run

From `extensions/molecule`:

```bash
ln -sfn . molecule
molecule test -s integration_satellite_content_view_create
```

For full integration against Satellite:

```bash
export SATELLITE_URL="https://satellite.example.com"
export SATELLITE_USERNAME="admin"
export SATELLITE_PASSWORD="your-password"
export SATELLITE_ORGANIZATION="MyOrg"
export SATELLITE_CONTENT_VIEW="molecule-satellite-content-view"
molecule prepare -s integration_satellite_content_view_create
molecule converge -s integration_satellite_content_view_create
molecule idempotence -s integration_satellite_content_view_create
molecule verify -s integration_satellite_content_view_create
molecule destroy -s integration_satellite_content_view_create
```
