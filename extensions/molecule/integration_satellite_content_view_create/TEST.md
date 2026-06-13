# Molecule Tests — integration_satellite_content_view_create

**Default CI test sequence**

verify

## What these tests cover

1. **Verify**
   - Runs `scripts/verify_readme.py` against `roles/satellite_content_view/README.md`
     using `docs/templates/role_readme_format_template.md`.

## Full integration sequence (manual)

prepare → converge → idempotence → verify → destroy

The destroy stage uses `satellite_content_view_destroy_create.yml` and skips
when `SATELLITE_*` credentials are not configured.

## Prerequisites

- Ansible and Molecule installed on the controller.
- Collection installed locally: `ansible-galaxy collection install . --force -p ~/.ansible/collections`
- For full integration against Satellite:
  - `redhat.satellite` installed from Red Hat Automation Hub (see role README Role Requirements)
  - Network access and credentials with Content View permissions

## Environment variables

| Variable                 | Required | Description                                                         |
| ------------------------ | -------- | ------------------------------------------------------------------- |
| `SATELLITE_URL`          | Yes      | Satellite server URL                                                |
| `SATELLITE_USERNAME`     | Yes      | Satellite API username                                              |
| `SATELLITE_PASSWORD`     | Yes      | Satellite API password                                              |
| `SATELLITE_ORGANIZATION` | Yes      | Satellite organization name                                         |
| `SATELLITE_CONTENT_VIEW` | No       | Test Content View name (default: `molecule-satellite-content-view`) |

## Commands

From `extensions/molecule`:

```bash
ln -sfn . molecule
molecule test -s integration_satellite_content_view_create
```

## Related scenarios

- `integration_satellite_content_view_publish`
- `integration_satellite_content_view_promote`

Run the create scenario before publish and promote so the test Content View exists.
