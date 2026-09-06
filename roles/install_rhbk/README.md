# Role: infra.ado.install_rhbk

Install **Red Hat Build of Keycloak (RHBK)** — Red Hat's supported Keycloak
distribution. This role never installs upstream Keycloak.

## Role Author

Automation Development Office

## ✅ Role Requirements

| Platform | Requirements |
|----------|--------------|
| `openshift` (default) | `kubernetes.core`, cluster credentials, RHBK operator catalog |
| `rhel` / `standalone` | Target RHEL host with dnf (Java 21 + unzip), and one zip source: HTTP/Satellite URL, git repo, or bootstrap `files/` zip copied by Contoller |

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `install_rhbk_platform` | `openshift`, `rhel`, or `standalone` |
| `name_space` | OpenShift namespace (default `keycloak`) |
| `ocp_rhbk_hostname` | Route hostname for Keycloak |
| `rhbk_hostname` | Standalone hostname (`KC_HOSTNAME`) |
| `rhbk_admin_password` / `rhbk_db_password` | Admin and Postgres passwords |
| `install_rhbk_standalone_zip_source` | `url`, `git`, or `upload` (empty = legacy auto-detect) |
| `install_rhbk_standalone_zip_url` | HTTP(S) URL the Keycloak host downloads (e.g. Satellite `/pub/rhbk.zip`) |
| `install_rhbk_standalone_zip_git_repo` | Git clone URL on the Keycloak host |
| `install_rhbk_standalone_zip_git_path` | Path to the zip inside the cloned repo |
| `install_rhbk_standalone_zip_git_branch` | Optional branch or tag |
| `install_rhbk_standalone_zip` | Controller/bootstrap path copied to the host (`upload` source) |

Standalone install unpacks the official `rhbk-*.zip` **on the Keycloak host**. Contoller
does not unzip into the EE; upload only stages the zip into bootstrap `files/`.

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

### Standalone (RHEL) — Satellite / HTTP URL

```yaml
- hosts: keycloak_ado
  become: true
  roles:
    - role: infra.ado.install_rhbk
      vars:
        install_rhbk_platform: rhel
        rhbk_hostname: keycloak-ado.server.lab
        rhbk_admin_password: "{{ vault_rhbk_admin_password }}"
        install_rhbk_standalone_zip_source: url
        install_rhbk_standalone_zip_url: http://sat.server.lab/pub/rhbk-26.6.5.zip
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
