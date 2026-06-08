# Role: infra.ado.applications_grafana_create_datasource

This role configures a Grafana Prometheus datasource by discovering the
OpenShift Prometheus route, creating a service-account token secret, and
updating Grafana datasource settings.

## Requirements

- Kubernetes/OpenShift API access from the Ansible controller.
- `kubernetes.core` collection for Kubernetes resource operations.
- `community.grafana` collection for datasource management.
- Credentials to access the target Grafana instance.

## Role Variables

| Variable | Default | Description |
| --- | --- | --- |
| `applications_grafana_create_datasource_state` | `present` | Desired role action. Current task flow uses `present`. |
| `applications_grafana_create_datasource_name` | `prometheus` | Grafana datasource name. |
| `applications_grafana_create_datasource_hostname` | `""` | Grafana hostname (without scheme). |
| `applications_grafana_create_datasource_admin_user` | `""` | Grafana admin username. |
| `applications_grafana_create_datasource_admin_password` | `""` | Grafana admin password. |
| `applications_grafana_create_datasource_validate_certs` | `false` | Whether to validate Grafana TLS certificates. |
| `applications_grafana_create_datasource_tls_skip_verify` | `true` | Whether datasource TLS verification is skipped. |
| `applications_grafana_create_datasource_prometheus_route_name` | `prometheus-k8s` | Prometheus Route name in OpenShift. |
| `applications_grafana_create_datasource_prometheus_route_namespace` | `openshift-monitoring` | Namespace containing the Prometheus Route and token Secret. |
| `applications_grafana_create_datasource_serviceaccount_name` | `grafana-prometheus-sa` | Service account used for Prometheus bearer token issuance. |
| `applications_grafana_create_datasource_serviceaccount_token_secret_name` | `grafana-prometheus-sa-token` | Name of the service-account-token Secret to create/read. |

### Compatibility aliases

The role currently supports these legacy aliases and normalizes them internally:

- `state` -> `applications_grafana_create_datasource_state`
- `grafana_datasource` -> `applications_grafana_create_datasource_name`
- `grafana_hostname` -> `applications_grafana_create_datasource_hostname`
- `grafana_admin_user` -> `applications_grafana_create_datasource_admin_user`
- `grafana_admin_password` -> `applications_grafana_create_datasource_admin_password`
- `grafana_validate_certs` -> `applications_grafana_create_datasource_validate_certs`
- `grafana_tls_skip_verify` -> `applications_grafana_create_datasource_tls_skip_verify`
- `grafana_prometheus_route_name` -> `applications_grafana_create_datasource_prometheus_route_name`
- `grafana_prometheus_route_namespace` -> `applications_grafana_create_datasource_prometheus_route_namespace`
- `grafana_prometheus_serviceaccount_name` -> `applications_grafana_create_datasource_serviceaccount_name`
- `grafana_prometheus_sa_token_secret_name` -> `applications_grafana_create_datasource_serviceaccount_token_secret_name`

## Example

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.applications_grafana_create_datasource
      vars:
        applications_grafana_create_datasource_state: present
        applications_grafana_create_datasource_name: prometheus
        applications_grafana_create_datasource_hostname: grafana.example.com
        applications_grafana_create_datasource_admin_user: admin
        applications_grafana_create_datasource_admin_password: "{{ vault_grafana_admin_password }}"
```

## Molecule Testing

This role uses an extension-level integration scenario:

- `extensions/molecule/integration_applications_grafana_create_datasource/molecule.yml`

Shared playbooks are located at:

- `extensions/molecule/utils/playbooks/applications_grafana_create_datasource_prepare.yml`
- `extensions/molecule/utils/playbooks/applications_grafana_create_datasource_converge.yml`
- `extensions/molecule/utils/playbooks/applications_grafana_create_datasource_verify.yml`
- `extensions/molecule/utils/playbooks/applications_grafana_create_datasource_destroy.yml`

Run from `extensions/molecule`:

```bash
molecule test -s integration_applications_grafana_create_datasource
```
