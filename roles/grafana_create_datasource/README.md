# Role: infra.ado.grafana_create_datasource

Creates Grafana Prometheus datasources via the Grafana HTTP API
(`community.grafana.grafana_datasource`), after ensuring an OpenShift
ServiceAccount token Secret (or using an explicit remote bearer token).

## Role Author

Automation Development Office.

## ✅ Role Requirements

- Kubernetes/OpenShift API access from the Ansible controller.
- `kubernetes.core` and `community.grafana` collections.
- Grafana admin credentials (`grafana_admin_user` / `grafana_admin_password`).

## 📦 Role Variables

| Variable | Default | Description |
| --- | --- | --- |
| `grafana_datasources` | `[]` | List of datasource definitions. When empty, one DS is created from `grafana_datasource`. |
| `grafana_datasource` | `Openshift-Prod` | Legacy single datasource name. |
| `grafana_hostname` | `""` | Grafana hostname (no scheme). |
| `grafana_admin_user` / `grafana_admin_password` | admin / `""` | Grafana basic auth. |

### `grafana_datasources` item fields

| Field | Description |
| --- | --- |
| `name` | Grafana datasource name (`Openshift-Prod`, `Openshift-Dev`, …). |
| `prometheus_url` | Optional absolute Prometheus URL (skips Route discovery). |
| `bearer_token` | Optional bearer token (skips SA token Secret). |
| `bearer_token_secret` | Optional `{name, namespace, key}` to read the token from a Kubernetes Secret (e.g. `grafana-openshift-dev-prometheus`). |
| `prometheus_route_name` / `prometheus_route_namespace` | Route overrides (default `thanos-querier` / `openshift-monitoring` so user-workload metrics are included). |
| `serviceaccount_name` / `serviceaccount_token_secret_name` | SA / Secret overrides. |

## 🚀 Role Usage

```yaml
- hosts: localhost
  roles:
    - role: infra.ado.grafana_create_datasource
      vars:
        grafana_hostname: grafana.apps.example.com
        grafana_admin_user: admin
        grafana_admin_password: "{{ vault_grafana_admin_password }}"
        grafana_datasources:
          - name: Openshift-Prod
            prometheus_route_name: thanos-querier
          - name: Openshift-Dev
            prometheus_url: https://prometheus-k8s-openshift-monitoring.apps.ocp.dev.example.com
            bearer_token_secret:
              name: grafana-openshift-dev-prometheus
              namespace: grafana
              key: token
```

Defaults in `components_defaults.yml` create both `Openshift-Prod` (local
`thanos-querier`) and `Openshift-Dev` (remote URL + token Secret).

Prefer **GrafanaDatasource** CRs (grafana-operator) in live clusters so the
operator owns reconciliation; this role remains the ADO playbook path for
API-based create/update.

## 🧪 Role Molecule Testing

No Molecule scenario ships with this role yet. Validate via Contoller JT
`ado-grafana-deploy-datasource-bootstrap` or the Grafana deploy workflow.

## 📁 Role Structure

```text
grafana_create_datasource/
├── defaults/main.yml
├── tasks/main.yml
├── tasks/grafana-manage-datasource.yml
└── README.md
```
