# Role: infra.ado.grafana_install

Deploy Grafana on OpenShift using the Grafana Operator, including persistent storage,
admin credentials, an optional Keycloak OIDC integration, and an OpenShift Route. When
`state: absent`, the role removes the Grafana custom resource and route.

## Role Author

- Chad Elliott
- Automation Development Office

## ✅ Role Requirements

- Red Hat OpenShift 4.x cluster with cluster-admin access
- Grafana Operator (`grafana-operator`) installed in the target namespace
- `kubernetes.core` collection installed
- Namespace, OperatorGroup, and Subscription for the Grafana Operator prepared before
  this role runs when installing from scratch

## 📦 Role Variables

| Variable | Description | Required | Default |
| --- | --- | --- | --- |
| `name_space` | Target OpenShift namespace where Grafana is deployed. | ✅ | — |
| `state` | `present` to install or `absent` to uninstall Grafana. | ❌ | `present` |
| `grafana_install_hostname` | Hostname used for the Grafana Route and server config. | ✅ | — |
| `grafana_install_admin_user` | Grafana admin username. | ✅ | — |
| `grafana_install_admin_password` | Grafana admin password. | ✅ | — |
| `storage_size` | PVC size for Grafana persistence. | ✅ | — |
| `storage_class` | Storage class for the Grafana PVC. | ✅ | — |
| `grafana_install_validate_certs` | Validate TLS when checking `/api/health`. | ❌ | `false` |
| `grafana_install_route_name` | OpenShift Route name for Grafana. | ❌ | `grafana` |
| `grafana_install_route_backend_svc` | Backend service name for the Route. | ❌ | `grafana-service` |
| `grafana_install_route_tls_termination` | Route TLS termination mode. | ❌ | `edge` |
| `route_insecure_edge_policy` | Route `insecureEdgeTerminationPolicy` value. | ❌ | `Redirect` |
| `oidc` | Optional Keycloak OIDC settings (`enabled`, `client_id`, `role_map`, etc.). | ❌ | — |
| `grafana_install_bearer_token` | Output fact: Prometheus bearer token set by the role. | ❌ | set by role |

### Auth via environment

Set kube auth via environment before running Molecule or playbooks:

```bash
export K8S_AUTH_HOST="https://api.ocp.example:6443"
export K8S_AUTH_API_KEY="..."
export K8S_AUTH_VERIFY_SSL="no"
```

## 🚀 Role Usage

```yaml
- name: Deploy Grafana using Operator
  hosts: localhost
  gather_facts: false
  vars:
    name_space: grafana
    grafana_install_hostname: grafana.apps.example.com
    grafana_install_admin_user: admin
    grafana_install_admin_password: supersecret
    storage_size: 5Gi
    storage_class: synology-iscsi-storage
    state: present
  roles:
    - role: infra.ado.grafana_install

- name: Delete Grafana using Operator
  hosts: localhost
  gather_facts: false
  vars:
    name_space: grafana
    state: absent
  roles:
    - role: infra.ado.grafana_install
```

## 🧪 Role Molecule Testing

The Molecule scenario lives at `roles/grafana_install/molecule/default`.

Run from the role directory:

```bash
cd roles/grafana_install
molecule test
```

For cluster integration, export `K8S_AUTH_*` variables before converge.

## 📁 Role Structure

```text
grafana_install/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   ├── main.yml
│   ├── install-grafana-operator.yml
│   └── delete-grafana-operator.yml
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/
    └── main.yml
```
