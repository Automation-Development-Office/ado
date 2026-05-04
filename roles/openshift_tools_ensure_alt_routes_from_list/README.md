# Role: ado.openshift_infrastructure_automation.rhbk

This role deploys the Red Hat Build of Keycloak (RHBK) on OpenShift, including the PostgreSQL backend, required Kubernetes Secrets, TLS, and the Keycloak Custom Resource. It is intended to be used as part of a modular OpenShift automation workflow.

## ✅ Role Requirements

- Red Hat OpenShift 4.x cluster with cluster-admin access
- Keycloak Operator (`rhbk-operator`) installed in the target namespace
- The following collections installed:
  - `kubernetes.core`
- The following components created ahead of this role:
  - Namespace where RHBK will be deployed
  - OperatorGroup and Subscription for the Keycloak Operator
  - TLS certificate and key (self-signed or signed by internal CA)

## 📦 Role Variables

| Variable             | Description                                                        | Required | Default |
|----------------------|--------------------------------------------------------------------|----------|---------|
| `name_space`         | Target OpenShift namespace where Keycloak will be deployed         | ✅       | —       |
| `rhbk_hostname`      | Public route hostname for Keycloak                                 | ✅       | —       |
| `tls_crt`            | TLS certificate for Keycloak ingress                               | ✅       | —       |
| `tls_key`            | TLS private key for Keycloak ingress                               | ✅       | —       |
| `rhbk_db_user`       | Username for PostgreSQL database (in the secret)                   | ✅       | —       |
| `rhbk_db_password`   | Password for PostgreSQL database (in the secret)                   | ✅       | —       |
| `storage`            | Storage class for the PostgreSQL StatefulSet                       | ✅       | —       |
| `postgres_image`     | Optional PostgreSQL image (defaults to RHEL9 PostgreSQL 15 image)  | ❌       | `registry.redhat.io/rhel9/postgresql-15:latest` |

---

## 📘 Example Usage

```yaml
- name: Deploy Red Hat Build of Keycloak
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    name_space: keycloak
    rhbk_hostname: keycloak.apps.ocp.server.lab
    tls_crt: "{{ lookup('file', 'certs/keycloak.crt') }}"
    tls_key: "{{ lookup('file', 'certs/keycloak.key') }}"
    rhbk_db_user: postgres
    rhbk_db_password: postgres
    storage: synology-iscsi-storage
  roles:
    - role: ado.openshift_infrastructure_automation.rhbk

```

**Structure**
rhbk/
├── defaults/main.yml
├── vars/main.yml
├── tasks/
│   ├── main.yml
│   ├── secrets.yml
│   ├── postgres.yml
│   └── keycloak_cr.yml
├── handlers/main.yml
├── files/
├── templates/
├── tests/
│   ├── inventory
│   └── test.yml
└── README.md