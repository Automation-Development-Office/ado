# Role: `satellite_oidc`

This Ansible role wires a Red Hat Satellite server to Keycloak / Red Hat build of Keycloak (RHBK) for OpenID Connect login.

It creates the confidential OIDC client with `infra.ado.rhbk_client` (default client id `ado-satellite` in realm `rhlab`), fetches the client secret, enables Foreman Keycloak on the Satellite host, and applies Satellite OIDC settings (`authorize_login_delegation`, issuer, audience, JWKS, logout URL).

> **Note:**
> Run this role against the Satellite server after install. Keycloak API calls are delegated to localhost. Satellite API credentials are required for Hammer/settings.

## Role Author

- Automation Development Office (automation-development-office@redhat.com)

## Role Requirements

- Ansible >= 2.16
- Target host: Red Hat Satellite server
- Privileged access on the Satellite host (`become: true`) for `satellite-installer`, Apache, and Hammer
- Required collections: `infra.ado` (`rhbk_client`), `community.general`
- Keycloak admin credentials when creating or fetching the client secret
- Satellite administrator credentials for Hammer OIDC settings

## Role Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `satellite_oidc_state` | `present` or `absent` | `present` |
| `satellite_oidc_create_client` | Create/update the Keycloak client with `infra.ado.rhbk_client` | `true` |
| `satellite_oidc_configure_satellite` | Enable OIDC on the Satellite host | `true` |
| `satellite_oidc_client_id` | Keycloak client id | `ado-satellite` |
| `satellite_oidc_realm` | Keycloak realm | `rhlab` |
| `satellite_oidc_keycloak_url` | Keycloak base URL | `https://keycloak.apps.ocp.prod.rhlab` |
| `satellite_oidc_issuer` | OIDC issuer URL. Derived from hostname + realm when empty | `""` |
| `satellite_oidc_client_secret` | Existing client secret. Fetched from Keycloak when empty | `""` |
| `satellite_oidc_admin_user` | Keycloak admin user | `rhbk_admin_user` / `admin` |
| `satellite_oidc_admin_password` | Keycloak admin password | `rhbk_admin_password` |
| `satellite_oidc_server_url` | Satellite URL used for redirect URIs and API | `satellite_config_server_url` |
| `satellite_oidc_username` | Satellite API username | `satellite_config_username` / `admin` |
| `satellite_oidc_password` | Satellite API password | `satellite_config_password` |
| `satellite_oidc_run_installer` | Run `satellite-installer --foreman-keycloak` | `true` |

`rhbk_hostname`, `rhbk_realm`, `rhbk_admin_user`, and `rhbk_admin_password` from the RHBK bootstrap vars are accepted as fallbacks.

## Role Usage

### Bootstrap Usage

#### ado-configure-satellite-oidc-bootstrap.yml

```yaml
- name: ADO | Configure Satellite Keycloak OIDC
  hosts: all
  gather_facts: true
  become: true
  vars_files:
    - group_vars/all/{{ env }}/vault_satellite.yml
    - group_vars/all/{{ env }}/vars_satellite.yml
  roles:
    - role: infra.ado.satellite_oidc
```

## Role Molecule Testing

No dedicated Molecule scenario. Validate against a lab Satellite and the existing `rhlab` realm.

```bash
ansible-playbook -i sat.server.lab, playbooks/satellite/ado-configure-satellite-oidc-bootstrap.yml
```
