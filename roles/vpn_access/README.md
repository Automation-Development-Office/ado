# Role: infra.ado.vpn_access

Approve or deny ADO Cluster Portal lab VPN requests via AAP by creating IdM
users, UniFi VPN accounts, and sending Mailjet email notifications.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core with `community.general` (IdM user management)
- IdM admin credentials (`vault_idm_admin_password`)
- UniFi controller API credentials (API key or username/password)
- SMTP credentials for Mailjet or compatible relay
- AAP job template `ADO | Manage VPN Access` targeting localhost inventory

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `vpn_access_action` | Portal action: `approve` or `deny`. Default from `action` extra-var. |
| `vpn_access_actor` | Approver username for audit logging. |
| `vpn_access_username` | Requested VPN username. |
| `vpn_access_email` | Requester email address. |
| `vpn_access_profile` | Portal access profile (for example `lab-access`). |
| `vpn_access_create_idm` | Create IdM user on approve. Default `true`. |
| `vpn_access_create_unifi` | Create UniFi VPN account on approve. Default `true`. |
| `vpn_access_send_email` | Send approval/denial email. Default `true`. |
| `vpn_access_ipa_host` | IdM server hostname. |
| `vpn_access_unifi_url` | UniFi controller base URL. |
| `vpn_access_smtp_host` | SMTP server hostname. Default `in-v3.mailjet.com`. |

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  vars:
    action: approve
    actor: chelliot
    username: jdoe
    email: jdoe@example.com
    profile: lab-access
    vault_idm_admin_password: "{{ vault_idm_admin_password }}"
    unifi_api_key: "{{ vault_unifi_api_key }}"
    smtp_user: "{{ vault_smtp_user }}"
    smtp_password: "{{ vault_smtp_password }}"
  roles:
    - role: infra.ado.vpn_access
```

Bootstrap playbook: `playbooks/vpn/ado-manage-vpn-access-bootstrap.yml`

Portal launch extra-vars: `action`, `actor`, `request_id`, `username`, `email`,
`display_name`, `profile`, `reason`, and optional `deny_reason`.

## 🧪 Role Molecule Testing

This role integrates with live IdM, UniFi, and SMTP endpoints. No Molecule
scenario is shipped; test via the AAP job template with sandbox credentials.

```bash
ansible-playbook playbooks/vpn/ado-manage-vpn-access-bootstrap.yml \
  -e action=deny \
  -e username=testuser \
  -e email=test@example.com \
  --vault-password-file .vault_pass
```

## 📁 Role Structure

```text
roles/vpn_access/
  README.md
  defaults/
  meta/
  tasks/
    main.yml
    idm_user.yml
    unifi_user.yml
    notify_email.yml
```
