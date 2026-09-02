# Role: infra.ado.ocp_zabbix

Deploy a Zabbix monitoring stack on OpenShift (MariaDB, Zabbix server, and web UI)
with persistent storage and an OpenShift Route.

## Role Author

- Chad Elliott
- Automation Development Office

## ✅ Role Requirements

- Red Hat OpenShift 4.x cluster with cluster-admin access
- `kubernetes.core` collection installed
- Pull access to MariaDB and Zabbix container images

## 📦 Role Variables

| Variable | Description | Required | Default |
| --- | --- | --- | --- |
| `state` | `present` to install or `absent` to remove Zabbix. | ❌ | `present` |
| `zabbix_hostname` | Route hostname for the Zabbix web UI. | ✅ | `""` |
| `zabbix_storage_size` | PVC size for MariaDB and Zabbix data. | ❌ | `20Gi` |
| `zabbix_mariadb_image` | MariaDB container image. | ❌ | `registry.redhat.io/rhel9/mariadb-105:latest` |
| `zabbix_server_image` | Zabbix server container image. | ❌ | `zabbix/zabbix-server-mysql:ubuntu-7.0-latest` |
| `zabbix_web_image` | Zabbix web UI container image. | ❌ | `zabbix/zabbix-web-nginx-mysql:ubuntu-7.0-latest` |
| `zabbix_db_user` | Zabbix database user. | ❌ | `zabbix` |
| `zabbix_db_name` | Zabbix database name. | ❌ | `zabbix` |
| `zabbix_db_root_password` | MariaDB root password. | ❌ | set in defaults |
| `zabbix_db_password` | Zabbix database user password. | ❌ | set in defaults |

## 🚀 Role Usage

```yaml
- name: Deploy Zabbix on OpenShift
  hosts: localhost
  gather_facts: false
  vars:
    zabbix_hostname: zabbix.apps.example.com
    zabbix_db_password: "{{ vault_zabbix_db_password }}"
  roles:
    - role: infra.ado.ocp_zabbix
```

## 🧪 Role Molecule Testing

No dedicated Molecule scenario yet. Validate on a lab OpenShift cluster.

## 📁 Role Structure

```text
ocp_zabbix/
├── defaults/main.yml
├── meta/main.yml
└── tasks/
    └── main.yml
```
