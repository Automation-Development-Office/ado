# SPDX-License-Identifier: GPL-3.0-or-later
# Role: infra.ado.vpn_access
#
# Approve / deny ADO Cluster Portal lab VPN requests via AAP.
# Approve: create IdM user, create UniFi VPN account, email credentials.
# Deny: email denial notice.
#
# Typical AAP Job Template:
#   Name: ADO | Manage VPN Access
#   Playbook: playbooks/vpn/ado-manage-vpn-access-bootstrap.yml
#   Inventory: localhost / controller inventory
#   Credentials: IdM admin (or Machine + vault), UniFi API, Mailjet SMTP
#
# Portal launch extra_vars (also accepted as flat extra_vars):
#   action: approve|deny
#   actor: <approver username>
#   request_id, username, email, display_name, profile, reason
#   deny_reason: (optional, deny only)
#   env: prod (optional, for vault_idm.yml)
#
# Required from operators (see role defaults):
#   - vault_idm_admin_password / IdM host
#   - UniFi URL + API key OR user/password
#   - SMTP (Mailjet) user/password/from
#   - Confirm UniFi VPN type + API path if account create returns non-2xx
