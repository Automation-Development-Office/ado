# Role: platform_idm_replica

Installs/manages an IdM replica using `redhat.rhel_idm.ipareplica`.

This role currently performs:
- input validation in `tasks/main.yml`
- one module call to `redhat.rhel_idm.ipareplica` in `tasks/install-idm-replica.yml`

## Requirements

- Ansible Core 2.16+ (per role metadata)
- `redhat.rhel_idm` collection available
- Environment prerequisites for IdM replica installation (DNS/time/network/connectivity and upstream IdM requirements)

## Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `platform_idm_replica_state` | no | `present` | Desired state (`present` or `absent`). |
| `platform_idm_replica_hostname` | yes | `""` | Replica host FQDN/hostname passed to module. |
| `platform_idm_replica_domain` | yes | `""` | IdM DNS domain. |
| `platform_idm_replica_realm` | yes | `""` | Kerberos realm for IdM. |
| `platform_idm_replica_server` | yes | `""` | Existing IdM server used for replica enrollment. |
| `platform_idm_replica_principal` | no | `""` | Principal for authenticated enrollment flows (omitted when empty). |
| `platform_idm_replica_admin_password` | yes for `present` | `""` | IdM admin password (`password`). |
| `platform_idm_replica_dm_password` | yes for `present` | `""` | Directory Manager password (`dm_password`). |
| `platform_idm_replica_setup_dns` | no | `false` | Whether to configure integrated DNS on replica. |
| `platform_idm_replica_setup_ca` | no | `false` | Whether to configure CA services on replica. |
| `platform_idm_replica_no_host_dns` | no | `false` | Disable host DNS checks. |
| `platform_idm_replica_no_ntp` | no | `false` | Disable NTP configuration checks/steps. |
| `platform_idm_replica_ip_addresses` | no | `[]` | Optional list of IP addresses for replica setup. |
| `platform_idm_replica_auto_forwarders` | no | `false` | Automatically discover DNS forwarders. |
| `platform_idm_replica_forwarders` | no | `[]` | Explicit DNS forwarders list. |

## Behavior Notes

- Validation currently enforces:
  - `platform_idm_replica_state` must be `present` or `absent`
  - hostname/domain/realm/server must be non-empty
  - admin and DM passwords are required when state is `present`
- The replica task uses `no_log: true` to reduce sensitive data exposure in logs.

## Example Playbook

```yaml
- name: Manage IdM replica
  hosts: idm_replicas
  become: true
  roles:
    - role: infra.ado.platform_idm_replica
      vars:
        platform_idm_replica_state: present
        platform_idm_replica_hostname: "idm-replica01.example.com"
        platform_idm_replica_domain: "example.com"
        platform_idm_replica_realm: "EXAMPLE.COM"
        platform_idm_replica_server: "idm01.example.com"
        platform_idm_replica_admin_password: "{{ vault_ipa_admin_password }}"
        platform_idm_replica_dm_password: "{{ vault_ipa_dm_password }}"
        platform_idm_replica_setup_dns: false
        platform_idm_replica_setup_ca: false
```

## License

GPL-3.0-or-later
