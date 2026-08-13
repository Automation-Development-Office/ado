# Role: infra.ado.grafana_upload_alerts

Upload Grafana alert rule JSON files from folder sources to the Grafana
provisioning API.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core on a host with HTTPS access to Grafana
- Grafana API key with alert rule provisioning permissions
- Alert files under each folder's `alerts_path` as `.json` or `.json.j2`
- `grafana_folders` entries populated (for example from bootstrap env vars)

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `grafana_alerts_enabled` | When false, the role exits immediately. Default `false`. |
| `grafana_folders` | List of folder entries with `source`, `source_type`, `name`, and optional `alerts_path`. |
| `grafana_hostname` | Grafana hostname for API requests (without scheme). |
| `grafana_api_key` | Grafana API bearer token from vault or extra-vars. |

Each `grafana_folders` item supports:

| Field | Description |
|-------|-------------|
| `name` | Folder label used for temp paths and logging. |
| `source` | Local directory or git repository URL. |
| `source_type` | `path` (default) or `git`. |
| `alerts_path` | Subdirectory containing alert JSON. Default `alerts`. |

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  vars:
    grafana_alerts_enabled: true
    grafana_hostname: grafana.apps.example.com
    grafana_api_key: "{{ vault_grafana_api_key }}"
    grafana_folders:
      - name: openshift
        source_type: path
        source: /opt/grafana-content/openshift
        alerts_path: alerts
  roles:
    - role: infra.ado.grafana_upload_alerts
```

Plain `.json` files are uploaded as-is; `.json.j2` templates are rendered
before POST to `/api/v1/provisioning/alert-rules`.

## 🧪 Role Molecule Testing

This role targets live Grafana instances. No Molecule scenario is shipped; run
against a lab cluster after Grafana install and confirm alert rules in the
Grafana UI.

```bash
ansible-playbook playbooks/grafana/ado-grafana-alerts-bootstrap.yml \
  -e grafana_alerts_enabled=true \
  --vault-password-file .vault_pass
```

## 📁 Role Structure

```text
roles/grafana_upload_alerts/
  README.md
  meta/
  tasks/
    main.yml
    collect-folder-alerts.yml
    upload-alert-file.yml
```
