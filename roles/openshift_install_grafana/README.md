# Role: ado.openshift_infrastructure_automation.grafana

This role deploys Grafana on OpenShift using the Grafana Operator, including persistent storage and secure admin credentials. It also creates an OpenShift `Route` to expose the Grafana web UI. When `state: absent`, it cleanly deletes the Grafana custom resource and the route.

## ✅ Role Requirements

- Red Hat OpenShift 4.x cluster with cluster-admin access
- Grafana Operator (`grafana-operator`) installed in the target namespace
- The following collections installed:
  - `kubernetes.core`
- The following components created ahead of this role:
  - Namespace where Grafana will be deployed
  - openshift_tools_operator_groups and Subscription for the Grafana Operator

## 📦 Role Variables

| Variable               | Description                                                   | Required | Default |
|------------------------|---------------------------------------------------------------|----------|---------|
| `name_space`           | Target OpenShift namespace where Grafana will be deployed     | ✅       | —       |
| `grafana_admin_user`   | Username for Grafana admin login                              | ✅       | —       |
| `grafana_admin_password` | Password for Grafana admin login                           | ✅       | —       |
| `storage_size`         | Size of the PVC used for persistence                          | ✅       | —       |
| `storage`              | Storage class name for the Grafana PVC                        | ✅       | —       |
| `state`                | Whether to `present` (install) or `absent` (uninstall) Grafana | ❌       | `present` |

---

## 📘 Example Usage (Install)

```yaml
- name: Deploy Grafana using Operator
  hosts: localhost
  gather_facts: false
  vars:
    name_space: grafana
    grafana_admin_user: admin
    grafana_admin_password: supersecret
    storage_size: 5Gi
    storage: synology-iscsi-storage
    state: present
  roles:
    - role: ado.openshift_infrastructure_automation.grafana

- name: Delete Grafana using Operator
  hosts: localhost
  gather_facts: false
  vars:
    name_space: grafana
    state: absent
  roles:
    - role: ado.openshift_infrastructure_automation.grafana
```

**Structure:**
```
grafana/
├── defaults/main.yml
├── vars/main.yml
├── tasks/main.yml
├── templates/
├── handlers/main.yml
├── files/
├── tests/
│   ├── inventory
│   └── test.yml
└── README.md
```