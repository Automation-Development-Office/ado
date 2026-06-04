# Role: idm_dns

Manages IdM DNS A records using `redhat.rhel_idm.dnsrecord`.

This role is intentionally focused and currently does:
- input validation in `tasks/main.yml`
- one module call to `redhat.rhel_idm.dnsrecord` in `tasks/idm_add_dns_entry.yml`

## Requirements

- Ansible Core 2.16+ (per role metadata)
- `redhat.rhel_idm` collection available
- Connectivity and permissions to manage records in the target IdM environment

## Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `idm_dns_state` | no | `present` | Desired record state (`present` or `absent`). |
| `idm_dns_zone` | yes | `""` | DNS zone name in IdM. |
| `idm_dns_record` | yes | `""` | Record name in the zone. |
| `idm_dns_ip_address` | yes | `""` | IPv4 address used for A record value. |
| `idm_dns_record_ttl` | no | `3600` | TTL for the DNS record. |
| `idm_dns_validate_certs` | no | `false` | TLS certificate validation toggle for API calls. |
| `idm_dns_ipa_host` | no | `""` | Optional explicit IPA host override. |
| `idm_dns_ipa_user` | no | `""` | Optional explicit IPA user override. |
| `idm_dns_ipa_pass` | no | `""` | Optional explicit IPA password override. |

## Behavior Notes

- Validation currently enforces:
  - `idm_dns_state` must be `present` or `absent`
  - `idm_dns_zone`, `idm_dns_record`, and `idm_dns_ip_address` must be non-empty
- The module task is marked `no_log: true` to avoid leaking credentials in logs.

## Example Playbook

```yaml
- name: Manage IdM DNS A record
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.idm_dns
      vars:
        idm_dns_state: present
        idm_dns_zone: "example.com"
        idm_dns_record: "app01"
        idm_dns_ip_address: "192.0.2.25"
        idm_dns_record_ttl: 3600
        idm_dns_validate_certs: false
        idm_dns_ipa_host: "idm01.example.com"
        idm_dns_ipa_user: "admin"
        idm_dns_ipa_pass: "{{ vault_idm_admin_password }}"
```

## License

GPL-3.0-or-later
