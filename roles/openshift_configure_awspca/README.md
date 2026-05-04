# Role: ado.openshift_infrastructure_automation.cert_manager_rootca

This role injects a Root Certificate Authority (CA) into OpenShift's cert-manager and configures it as a ClusterIssuer or namespaced Issuer. It enables cert-manager to issue certificates signed by your internal CA across the OpenShift cluster.

**Author**: Chad Elliott

---

## ✅ Role Requirements

- Requires a working cert-manager deployment in the specified namespace (typically `cert-manager`).
- Assumes `kubernetes.core` collection is installed.
- Requires valid TLS cert and key content provided as Ansible variables.
- You must have sufficient RBAC permissions to create Secrets and Issuers/ClusterIssuers.

---

## 📦 Role Variables

| Variable                                | Description                                                                 | Required | Default              |
|-----------------------------------------|-----------------------------------------------------------------------------|----------|----------------------|
| `name_space`                            | Namespace to place the root CA secret and/or namespaced Issuer              | ✅       | —                    |
| `state`                                 | Whether to create (`present`) or delete (`absent`) the resources            | ✅       | `present`            |
| `tls_crt`                               | Root CA certificate (PEM format, multiline string)                          | ✅       | —                    |
| `tls_key`                               | Root CA private key (PEM format, multiline string)                          | ✅       | —                    |
| `cert_manager_root_ca_secret_name`      | Name of the secret that will store the CA certificate and key               | ❌       | `root-ca-secret`     |
| `cert_manager_root_ca_issuer_name`      | Name of the cert-manager issuer or clusterissuer to create                  | ❌       | `root-ca-issuer`     |
| `cert_manager_root_ca_is_cluster_issuer`| Whether to create a ClusterIssuer (`true`) or namespaced Issuer (`false`)   | ❌       | `true`               |

---

## 🚀 Example Usage

```yaml
- name: Configure cert-manager with custom root CA
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yml
  vars:
    name_space: cert-manager
    state: present
    cert_manager_root_ca_secret_name: root-ca-secret
    cert_manager_root_ca_issuer_name: root-ca-issuer
    cert_manager_root_ca_is_cluster_issuer: true
    tls_crt: "{{ vault_cert }}"
    tls_key: "{{ vault_key }}"
  roles:
    - role: ado.openshift_infrastructure_automation.cert_manager_rootca


**Structure:**
```
cert-manager/
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

**Example vault.yml**
```
vault_cert: |
  -----BEGIN CERTIFICATE-----
  ...
  -----END CERTIFICATE-----

vault_key: |
  -----BEGIN PRIVATE KEY-----
  ...
  -----END PRIVATE KEY-----

```