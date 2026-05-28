# Role: platform_content_view

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

## Variables

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
    - role: platform_content_view
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
    - role: platform_content_view
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
    - role: platform_content_view
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

- `platform_content_view_create_result` (create action)
- `platform_content_view_publish_result` (publish action)
- `platform_content_view_promote_result` (promote action)

## Role Layout

```text
roles/platform_content_view/
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
```

## License

GPL-3.0-or-later

## Authors

Jeff Radabaugh
Chris Kirk