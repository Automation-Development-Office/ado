# Role: platform_idm_client

Registers an IPA/IdM client using `redhat.rhel_idm.ipaclient`.

This role is intentionally small. It imports `tasks/idm_register_client.yml`, which currently runs one module call:

- `redhat.rhel_idm.ipaclient`
- `state: "{{ state }}"`
- `force: true`

## Requirements

- Ansible Core 2.16+ (per role metadata)
- `redhat.rhel_idm` collection available
- Host/network prerequisites required by the IPA client module (DNS/time/connectivity and credentials as applicable to your environment)

## Variables

| Variable | Required | Description |
| --- | --- | --- |
| `state` | yes | Desired IPA client state passed directly to `redhat.rhel_idm.ipaclient` (for example, `present` or `absent`). |

## Behavior Notes

- The role currently exposes only `state` and hard-sets `force: true`.
- Additional `redhat.rhel_idm.ipaclient` options are not surfaced in this role yet.
- Complexity is mostly environmental (IPA server reachability, auth, DNS/time setup), not in role logic.

## Example Playbook

```yaml
- name: Manage IPA client registration
  hosts: all
  become: true
  roles:
    - role: infra.ado.platform_idm_client
      vars:
        state: present
```

## License

See `meta/main.yml` for current role license metadata.
