# Role: infra.ado.install_rhbk

Install **Red Hat Build of Keycloak (RHBK)** — Red Hat's supported Keycloak
distribution. This role never installs upstream Keycloak.

## Platforms

| `install_rhbk_platform` | What runs |
|-------------------------|-----------|
| `openshift` (default)   | Operator + Keycloak CR + Postgres on OpenShift |
| `rhel` / `standalone`   | Podman containers on RHEL VM/bare metal |

## Standalone (RHEL) example

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
        # registry.redhat.io pull (or pre-load authfile on the host)
        rhbk_registry_user: "{{ vault_rh_registry_user | default('') }}"
        rhbk_registry_password: "{{ vault_rh_registry_password | default('') }}"
```

Image defaults to `registry.redhat.io/rhbk/keycloak-rhel9:26.2`.

## OpenShift example

```yaml
- hosts: localhost
  roles:
    - role: infra.ado.install_rhbk
      vars:
        install_rhbk_platform: openshift
        name_space: keycloak
        ocp_rhbk_hostname: keycloak.apps.ocp.prod.rhlab
```
