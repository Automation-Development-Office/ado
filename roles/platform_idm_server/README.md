# Role: platform_idm_server

Installs/manages an IdM server using `redhat.rhel_idm.ipaserver`.

This role is intentionally small and currently performs:
- input validation
- one module call to `redhat.rhel_idm.ipaserver`

## Requirements

- Ansible Core 2.16+ (per role metadata)
- `redhat.rhel_idm` collection available
- Host/network prerequisites for IdM server installation based on your environment

## Role Variables

### Canonical role variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `platform_idm_server_state` | no | `present` | Desired state (`present` or `absent`). |
| `platform_idm_server_name` | yes | `""` | IdM server host/name passed to `ipaserver`. |
| `platform_idm_server_ipaadmin_password` | yes for `present` | `""` | IPA admin password used by module. |

## Behavior Notes

- Validation fails early if:
  - state is not `present`/`absent`
  - server name is missing
  - password is missing for `present` state
- Module keys remain native (`state`, `name`, `ipaadmin_password`) while role vars are namespaced to avoid collisions when included from other roles.

## Example Playbook

```yaml
- name: Manage IdM server
  hosts: idm_servers
  become: true
  roles:
    - role: infra.ado.platform_idm_server
      vars:
        platform_idm_server_state: present
        platform_idm_server_name: "idm01.example.com"
        platform_idm_server_ipaadmin_password: "{{ vault_ipa_admin_password }}"
```

## License

GPL-3.0-or-later
