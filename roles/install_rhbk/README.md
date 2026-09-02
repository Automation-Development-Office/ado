# Role: infra.ado.install_rhbk

Install **Red Hat Build of Keycloak (RHBK)** — Red Hat's supported Keycloak
distribution. This role never installs upstream Keycloak.

## Role Author

Automation Development Office

## ✅ Role Requirements

| Platform | Requirements |
|----------|--------------|
| `openshift` (default) | `kubernetes.core`, cluster credentials, RHBK operator catalog |
| `rhel` / `standalone` | Podman on RHEL, `registry.redhat.io` pull or pre-loaded authfile |

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `install_rhbk_platform` | `openshift`, `rhel`, or `standalone` |
| `name_space` | OpenShift namespace (default `keycloak`) |
| `ocp_rhbk_hostname` | Route hostname for Keycloak |
| `rhbk_hostname` | Standalone hostname |
| `rhbk_admin_password` / `rhbk_db_password` | Admin and Postgres passwords |
| `rhbk_registry_user` / `rhbk_registry_password` | Optional pull secret for standalone |

Standalone image default: `registry.redhat.io/rhbk/keycloak-rhel9:26.2`.

## 🚀 Role Usage

### OpenShift

```yaml
- hosts: localhost
  roles:
    - role: infra.ado.install_rhbk
      vars:
        install_rhbk_platform: openshift
        name_space: keycloak
        ocp_rhbk_hostname: keycloak.apps.ocp.prod.rhlab
```

### Standalone (RHEL)

```yaml
- hosts: keycloak_ado
  become: true
  roles:
    - role: infra.ado.install_rhbk
      vars:
        install_rhbk_platform: rhel
        rhbk_hostname: keycloak-ado.server.lab
        rhbk_admin_password: "{{ vault_rhbk_admin_password }}"
        rhbk_db_password: "{{ vault_rhbk_db_password }}"
```

Contoller JTs: `ado-install-rhbk-standalone-bootstrap`, RHBK deploy/configure
workflow nodes after bootstrap.

## 🧪 Role Molecule Testing

No Molecule scenario ships with this role yet. Validate via RHBK workflow JTs
(install → realm → client scopes → clients) after bootstrap.

## 📁 Role Structure

```text
roles/install_rhbk/
  README.md
  defaults/main.yml
  meta/main.yml
  tasks/
    main.yml
    install-rhbk-operator.yml
    install-rhbk-standalone.yml
```
