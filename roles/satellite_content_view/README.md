# Role: satellite_content_view

Manages Red Hat Satellite Content Views with three actions:

- `create` - create the Content View
- `publish` - publish a new Content View version
- `promote` - promote a published version to lifecycle environments

## Requirements

- Ansible 2.9 or newer
- `redhat.satellite` collection installed
- Connectivity from controller to Satellite API
- Valid Satellite credentials with permissions for Content View operations

## Workflow

Role entrypoint `tasks/main.yml` dispatches by action:

1. `sat_content_view_action: create` -> imports `tasks/create_content_view.yml`
2. `sat_content_view_action: publish` -> imports `tasks/publish_content_view.yml`
3. `sat_content_view_action: promote` -> imports `tasks/promote_content_view.yml`

No task file runs unless both `content_view` and `sat_content_view_action` are defined.

## Role Variables

| Variable | Description | Required For |
| --- | --- | --- |
| `sat_content_view_action` | Action selector. Supported values: `create`, `publish`, `promote`. | All |
| `satellite_url` | URL of the Satellite server. | All |
| `satellite_username` | Satellite username. | All |
| `satellite_password` | Satellite password. | All |
| `organization` | Satellite organization name. | All |
| `content_view` | Name of the Satellite Content View. | All |
| `lifecycle_environments` | Target lifecycle environment(s). | Promote |
| `published_content_view` | Compatibility variable currently validated in promote flow. | Promote |
| `published_content_view_version` | Content View version to promote. | Promote |

## Example Playbooks

### Create Content View

```yaml
- name: Create Satellite Content View
  hosts: localhost
  gather_facts: false
  roles:
    - role: satellite_content_view
      sat_content_view_action: create
      satellite_url: "https://satellite.example.com"
      satellite_username: "admin"
      satellite_password: "password"
      organization: "MyOrg"
      content_view: "RHEL8_Base"
```

### Publish Content View

```yaml
- name: Publish Satellite Content View
  hosts: localhost
  gather_facts: false
  roles:
    - role: satellite_content_view
      sat_content_view_action: publish
      satellite_url: "https://satellite.example.com"
      satellite_username: "admin"
      satellite_password: "password"
      organization: "MyOrg"
      content_view: "RHEL8_Base"
```

### Promote Content View

```yaml
- name: Promote Satellite Content View
  hosts: localhost
  gather_facts: false
  roles:
    - role: satellite_content_view
      sat_content_view_action: promote
      satellite_url: "https://satellite.example.com"
      satellite_username: "admin"
      satellite_password: "password"
      organization: "MyOrg"
      content_view: "RHEL8_Base"
      lifecycle_environments:
        - "Library"
        - "Dev"
      published_content_view: "RHEL8_Base"
      published_content_view_version: "1.0"
```

## Returned Runtime Variables

- `satellite_content_view_create_result` (create action)
- `satellite_content_view_publish_result` (publish action)
- `satellite_content_view_promote_result` (promote action)

## Molecule Testing

Extension-level Molecule scenarios under `extensions/molecule/`:

| Scenario | Action | Command |
| --- | --- | --- |
| `integration_satellite_content_view_create` | create | `molecule test -s integration_satellite_content_view_create` |
| `integration_satellite_content_view_publish` | publish | `molecule test -s integration_satellite_content_view_publish` |
| `integration_satellite_content_view_promote` | promote | `molecule test -s integration_satellite_content_view_promote` |

Playbooks live in `extensions/molecule/utils/playbooks/` (`satellite_content_view_*`).

Export Satellite credentials before running full integration (prepare/converge/destroy):

```bash
export SATELLITE_URL="https://satellite.example.com"
export SATELLITE_USERNAME="admin"
export SATELLITE_PASSWORD="your-password"
export SATELLITE_ORGANIZATION="MyOrg"
export SATELLITE_CONTENT_VIEW="molecule-satellite-content-view"
```

Run from the collection `extensions/molecule` directory:

```bash
cd extensions/molecule
ln -sfn . molecule
molecule test -s integration_satellite_content_view_create
```

See `extensions/molecule/integration_satellite_content_view_create/README.md`
and `TEST.md` for details.

## Role Layout

```text
roles/satellite_content_view/
  README.md
  defaults/main.yml
  handlers/main.yml
  meta/main.yml
  tasks/main.yml
  tasks/create_content_view.yml
  tasks/publish_content_view.yml
  tasks/promote_content_view.yml
  tests/inventory
  vars/main.yml

extensions/molecule/
  integration_satellite_content_view_create/
  integration_satellite_content_view_publish/
  integration_satellite_content_view_promote/
  utils/playbooks/satellite_content_view_*.yml
```

## License

GPL-3.0-or-later

## Authors

Jeff Radabaugh
Chris Kirk
