# Role: infra.ado.grafana_upload_dashboards

Upload Grafana dashboard JSON files generated from templates and set their
datasource value before import.

## Role Author

Automation Development Office.

## ✅ Role Requirements

- `community.grafana` collection for `community.grafana.grafana_dashboard`.
- Reachable Grafana endpoint and valid credentials.
- Dashboard template files referenced by `grafana_dashboards`.

## 📦 Role Variables

Variables used by the role tasks:

- `state` (`present` expected to run upload tasks).
- `grafana_dashboards` (list of items with at least `name` and `template`).
- `grafana_datasource` (replacement datasource value in rendered JSON).
- `grafana_hostname` (Grafana host, scheme is set in the task as `https://`).
- `grafana_admin_user` (Grafana username).
- `grafana_admin_password` (Grafana password).
- `grafana_folder` (folder name for imported dashboards).

Notes:

- `defaults/main.yml` does not currently define role defaults.
- Role execution is gated in `tasks/main.yml` by `when: state == "present"`.

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.grafana_upload_dashboards
      vars:
        state: present
        grafana_hostname: grafana.example.com
        grafana_admin_user: admin
        grafana_admin_password: "{{ vault_grafana_admin_password }}"
        grafana_folder: General
        grafana_datasource: Openshift
        grafana_dashboards:
          - name: cluster-overview
            template: dashboards/cluster-overview.json.j2
```

## 🧪 Role Molecule Testing

There is no dedicated extension-level Molecule scenario for this role in the
current repository layout.

## 📁 Role Structure

```text
grafana_upload_dashboards/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   ├── main.yml
│   └── grafana-upload-dashboards.yml
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/
    └── main.yml
```
