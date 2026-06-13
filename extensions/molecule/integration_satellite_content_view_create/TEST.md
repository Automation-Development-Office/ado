# Molecule Tests — integration_satellite_content_view_create

**Default CI test sequence**

verify

## What these tests cover

1. **Verify**
   - Confirms `roles/satellite_content_view/README.md` exists.
   - Checks heading, variables table, example code block, and key sections.

## Full integration sequence (manual)

prepare → converge → idempotence → verify → destroy

## Prerequisites

- Ansible and Molecule installed on the controller.
- Network access to a Satellite server for converge/idempotence/destroy.
- `redhat.satellite` collection available.

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
