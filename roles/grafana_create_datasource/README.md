# Role: infra.ado.grafana_create_datasource

This role configures a Grafana Prometheus datasource by discovering the
OpenShift Prometheus route, creating a service-account token secret, and
updating Grafana datasource settings.

## Role Author

Automation Development Office.

## ✅ Role Requirements

- Kubernetes/OpenShift API access from the Ansible controller.
- `kubernetes.core` collection for Kubernetes resource operations.
- `community.grafana` collection for datasource management.
- Credentials to access the target Grafana instance.

## 📦 Role Variables

| Variable | Default | Description |
| --- | --- | --- |
| `grafana_create_datasource_state` | `present` | Desired role action. Current task flow uses `present`. |
| `grafana_create_datasource_name` | `prometheus` | Grafana datasource name. |
| `grafana_create_datasource_hostname` | `""` | Grafana hostname (without scheme). |
| `grafana_create_datasource_admin_user` | `""` | Grafana admin username. |
| `grafana_create_datasource_admin_password` | `""` | Grafana admin password. |
| `grafana_create_datasource_validate_certs` | `false` | Whether to validate Grafana TLS certificates. |
| `grafana_create_datasource_tls_skip_verify` | `true` | Whether datasource TLS verification is skipped. |
| `grafana_create_datasource_prometheus_route_name` | `prometheus-k8s` | Prometheus Route name in OpenShift. |
| `grafana_create_datasource_prometheus_route_namespace` | `openshift-monitoring` | Namespace containing the Prometheus Route and token Secret. |
| `grafana_create_datasource_serviceaccount_name` | `grafana-prometheus-sa` | Service account used for Prometheus bearer token issuance. |
| `grafana_create_datasource_serviceaccount_token_secret_name` | `grafana-prometheus-sa-token` | Name of the service-account-token Secret to create/read. |

### Compatibility aliases

The role currently supports these legacy aliases and normalizes them internally:

- `state` -> `grafana_create_datasource_state`
- `grafana_datasource` -> `grafana_create_datasource_name`
- `grafana_hostname` -> `grafana_create_datasource_hostname`
- `grafana_admin_user` -> `grafana_create_datasource_admin_user`
- `grafana_admin_password` -> `grafana_create_datasource_admin_password`
- `grafana_validate_certs` -> `grafana_create_datasource_validate_certs`
- `grafana_tls_skip_verify` -> `grafana_create_datasource_tls_skip_verify`
- `grafana_prometheus_route_name` -> `grafana_create_datasource_prometheus_route_name`
- `grafana_prometheus_route_namespace` -> `grafana_create_datasource_prometheus_route_namespace`
- `grafana_prometheus_serviceaccount_name` -> `grafana_create_datasource_serviceaccount_name`
- `grafana_prometheus_sa_token_secret_name` -> `grafana_create_datasource_serviceaccount_token_secret_name`

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.grafana_create_datasource
      vars:
        grafana_create_datasource_state: present
        grafana_create_datasource_name: prometheus
        grafana_create_datasource_hostname: grafana.example.com
        grafana_create_datasource_admin_user: admin
        grafana_create_datasource_admin_password: "{{ vault_grafana_admin_password }}"
```

## 🧪 Role Molecule Testing

This role uses an extension-level integration scenario:

- `extensions/molecule/integration_grafana_create_datasource/molecule.yml`

Shared playbooks are located at:

- `extensions/molecule/utils/playbooks/grafana_create_datasource_prepare.yml`
- `extensions/molecule/utils/playbooks/grafana_create_datasource_converge.yml`
- `extensions/molecule/utils/playbooks/grafana_create_datasource_verify.yml`
- `extensions/molecule/utils/playbooks/grafana_create_datasource_destroy.yml`

Run from `extensions/molecule`:

```bash
molecule test -s integration_grafana_create_datasource
```

## 📁 Role Structure

```text
grafana_create_datasource/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   ├── main.yml
│   └── grafana-manage-datasource.yml
└── vars/
    └── main.yml
```
