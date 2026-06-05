# Role: infra.ado.applications_elastic

This role performs operational checks/actions for Elasticsearch through a simple
state-driven interface.

Supported states:

- `start`: start Elasticsearch (systemd or custom command) and wait for HTTP readiness
- `balance`: verify the cluster is green and has no pending relocation/initialization
- `stop`: stop Elasticsearch via systemd or custom-process mode and report post-stop probe status
- `status`: query and print cluster health summary

## Requirements

- Network access from the controller to the Elasticsearch API endpoint.
- Optional system-level privileges if using the `start` path with systemd/custom process start.

## Role Variables

| Variable | Default | Description |
| --- | --- | --- |
| `applications_elastic_state` | `status` | Desired action: `start`, `balance`, `stop`, or `status`. |
| `applications_elastic_systemd_enabled` | `true` | Use systemd start path when state is `start`. |
| `applications_elastic_systemd_unit` | `elasticsearch` | Systemd unit name for the start action. |
| `applications_elastic_start_cmd` | `""` | Custom start command used when `applications_elastic_systemd_enabled` is `false`. |
| `applications_elastic_pid_file` | `/var/run/elasticsearch.pid` | PID file used for custom-start process tracking. |
| `applications_elastic_url` | `http://localhost:9200` | Elasticsearch base URL. |
| `applications_elastic_user` | `""` | Optional username for HTTP basic auth. |
| `applications_elastic_pass` | `""` | Optional password for HTTP basic auth. |
| `applications_elastic_http_timeout` | `60` | Timeout budget (seconds) used by HTTP readiness retries. |

### Compatibility aliases

To avoid breaking existing callers, the role currently accepts these legacy aliases
and normalizes them internally:

- `state` -> `applications_elastic_state`
- `es_systemd_enabled` -> `applications_elastic_systemd_enabled`
- `es_systemd_unit` -> `applications_elastic_systemd_unit`
- `es_start_cmd` -> `applications_elastic_start_cmd`
- `es_pid_file` -> `applications_elastic_pid_file`
- `es_url` -> `applications_elastic_url`
- `es_user` -> `applications_elastic_user`
- `es_pass` -> `applications_elastic_pass`
- `es_http_timeout` -> `applications_elastic_http_timeout`

## Examples

### Check cluster status

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.applications_elastic
      vars:
        applications_elastic_state: status
        applications_elastic_url: http://localhost:9200
```

### Check balance with auth

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.applications_elastic
      vars:
        applications_elastic_state: balance
        applications_elastic_url: https://elastic.example.com:9200
        applications_elastic_user: elastic
        applications_elastic_pass: "{{ vault_elastic_password }}"
```

### Stop Elasticsearch

```yaml
- hosts: localhost
  gather_facts: false
  become: true
  roles:
    - role: infra.ado.applications_elastic
      vars:
        applications_elastic_state: stop
        applications_elastic_systemd_enabled: true
        applications_elastic_systemd_unit: elasticsearch
```

For custom-process mode (`applications_elastic_systemd_enabled: false`), provide
`applications_elastic_start_cmd` and/or `applications_elastic_pid_file` so the role
can find and terminate the process safely.

## Molecule

This role's scenario is normalized at:

- `extensions/molecule/integration_applications_elastic/molecule.yml`

Shared playbooks are located at:

- `extensions/molecule/utils/playbooks/applications_elastic_prepare.yml`
- `extensions/molecule/utils/playbooks/applications_elastic_converge.yml`
- `extensions/molecule/utils/playbooks/applications_elastic_verify.yml`
- `extensions/molecule/utils/playbooks/applications_elastic_destroy.yml`

Run from `extensions/molecule`:

```bash
molecule test -s integration_applications_elastic
```

### Optional live checks in Molecule

By default, converge uses a safe non-live path. To execute real Elasticsearch
status checks during scenario runs:

```bash
export APPLICATIONS_ELASTIC_ENABLE_LIVE_CHECKS=true
export APPLICATIONS_ELASTIC_URL="http://localhost:9200"
molecule test -s integration_applications_elastic
```
