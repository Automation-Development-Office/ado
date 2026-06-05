# Role: infra.ado.rhel_ext_system_roles

This role is a thin wrapper around `redhat.rhel_system_roles` so callers can apply selected
system roles (for example `timesync`, `selinux`, `cockpit`) through a consistent interface.

- Driven by `sr_apply` and per-role inputs in `sr_vars`.
- Normalizes SELinux input values and policy handling.
- Uses safe defaults for timesync variables.
- Applies Cockpit when requested.

## Requirements

- `redhat.rhel_system_roles` must be available on the controller.

```bash
ansible-galaxy collection install redhat.rhel_system_roles
```

- Target hosts should be supported RHEL systems.
- Run with privilege escalation (`become: true`) when managing system settings.

## Variables

| Variable | Type | Description |
| --- | --- | --- |
| `sr_apply` | `list[str]` | Required list of short role keys to apply (`timesync`, `selinux`, `cockpit`). |
| `sr_vars` | `dict` | Optional per-role variable map keyed by entries in `sr_apply`. |
| `rhel_ext_system_roles_roles_map` | `dict` | Override map of short keys to upstream collection/role identifiers. |

### `sr_vars` details

SELinux (`redhat.rhel_system_roles.selinux`)

| Key | Type | Notes |
| --- | --- | --- |
| `selinux_state` | `string` | Accepts `enabled`, `disabled`, `enforcing`, `permissive`, `on`, `off`. |
| `selinux_policy` | `string` | Optional input; auto-filled when state requires it. |

Timesync (`redhat.rhel_system_roles.timesync`)

| Key | Type | Notes |
| --- | --- | --- |
| `timesync_ntp_servers` | `list[dict]` | Example: `[{hostname: 0.rhel.pool.ntp.org, iburst: true}]` |
| `timesync_ntp_provider` | `string` | `chrony` or `ntp`; empty string allows upstream auto-detection. |
| `timesync_ntp_servers_options` | `dict` | Provider-specific options. |

Cockpit (`redhat.rhel_system_roles.cockpit`)

No inputs are required for a basic install/enable flow.

## Examples

### Apply timesync, selinux, and cockpit

```yaml
- hosts: all
  become: true
  gather_facts: false
  tasks:
    - name: Apply selected RHEL system roles
      ansible.builtin.include_role:
        name: infra.ado.rhel_ext_system_roles
      vars:
        sr_apply:
          - timesync
          - selinux
          - cockpit
        sr_vars:
          timesync:
            timesync_ntp_servers:
              - hostname: 0.rhel.pool.ntp.org
                iburst: true
          selinux:
            selinux_state: permissive
            selinux_policy: targeted
```

### Apply only timesync

```yaml
- hosts: app
  become: true
  gather_facts: false
  tasks:
    - name: Apply timesync via wrapper
      ansible.builtin.include_role:
        name: infra.ado.rhel_ext_system_roles
      vars:
        sr_apply:
          - timesync
        sr_vars:
          timesync:
            timesync_ntp_servers:
              - hostname: 2.rhel.pool.ntp.org
                iburst: true
```

## Behavior Notes

- The role gathers a minimal fact subset so upstream roles behave correctly even when callers use `gather_facts: false`.
- SELinux values are normalized and a policy is chosen when required.
- Timesync variables avoid passing `omit` into upstream role data paths.

## Molecule

This role is tested from the extension-level Molecule scenario:
`extensions/molecule/integration_rhel_ext_system_roles`.

Scenario wiring is defined in:

- `extensions/molecule/integration_rhel_ext_system_roles/molecule.yml`
- `extensions/molecule/utils/playbooks/rhel_ext_system_roles_prepare.yml`
- `extensions/molecule/utils/playbooks/rhel_ext_system_roles_converge.yml`
- `extensions/molecule/utils/playbooks/rhel_ext_system_roles_verify.yml`
- `extensions/molecule/utils/playbooks/rhel_ext_system_roles_destroy.yml`

Run from `extensions/molecule`:

```bash
molecule test -s integration_rhel_ext_system_roles
```

## Authors

- Chad Elliott (<chelliot@redhat.com>)

## Repository layout (role)

```text
.
├── defaults
│   └── main.yml
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── README.md
├── tasks
│   └── main.yml
└── vars
    └── main.yml
```
