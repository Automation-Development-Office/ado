# Role: infra.ado.utilities_services_management

Manage the state (start/stop/restart/reload) and enable/disable settings of one or
more **system services** in a consistent, idempotent way.

- Accepts a list of `service_names` and a target `service_state`.
- **Smart unit resolution:** accepts names with or without the `.service` suffix.
- Optional `service_enabled` toggles enablement state.
- Skips cleanly when a given service isn’t present on the host.

---

## Requirements

- Target hosts reachable by Ansible (privileged account or `become: true` as needed).
- **Systemd-based hosts** are expected (facts are derived from systemd inventory).
- **Python ≥ 3.7 on managed hosts**. *Note:* Python **3.6 and older** cannot use `service_facts`, so this role will no‑op on those hosts.

---

## Variables

| Variable | Description |
| --- | --- |
| `service_names` | **Required.** A list of service names to manage (with or without `.service`). |
| `service_state` | **Required.** Desired state for each service. Common values: `started`, `stopped`, `restarted`, `reloaded`. |
| `service_enabled` | Optional boolean. If set, enables (`true`) or disables (`false`) each service. |

> The role gathers `service_facts` and manages only services present in `ansible_facts.services`.
> Names without `.service` are automatically mapped to their unit (e.g., `sshd` → `sshd.service`).

---

## Examples

### Start and enable multiple services

```yaml
- hosts: all
  gather_facts: false
  vars:
    service_names:
      - sshd
      - crond
    service_state: started
    service_enabled: true
  roles:
    - role: infra.ado.utilities_services_management
```

### Stop and disable a service

```yaml
- hosts: app_servers
  gather_facts: false
  vars:
    service_names:
      - httpd
    service_state: stopped
    service_enabled: false
  roles:
    - role: infra.ado.utilities_services_management
```

### Restart services without changing enablement

```yaml
- hosts: db_servers
  gather_facts: false
  vars:
    service_names:
      - tuned
      - firewalld
    service_state: restarted
  roles:
    - role: infra.ado.utilities_services_management
```

---

## Behavior Notes

- Uses `ansible.builtin.service_facts` to discover available services.
- For each name in `service_names`, the role manages it **only if** the service (or `${name}.service`) exists in `ansible_facts.services`.
- On non‑systemd hosts (or where `service_facts` is unavailable), the role performs no changes.
- Operations are idempotent; repeated runs won’t introduce changes unless service state drifts.

---

## Molecule

This role is tested using the extension-level Molecule scenario:

- `integration_utilities_services_management`

Scenario definition lives under `extensions/molecule/integration_utilities_services_management/`,
and shared scenario playbooks are under `extensions/molecule/utils/playbooks/`:

- `utilities_services_management_prepare.yml`
- `utilities_services_management_converge.yml`
- `utilities_services_management_verify.yml`
- `utilities_services_management_destroy.yml`

The scenario test sequence is:

```text
prepare → converge → idempotence → verify
```

Destroy sequence:

```text
destroy
```

---

## Author

- Chad Elliott (<chelliot@redhat.com>)

---

## Repository layout (role)

```text
.
├── defaults
│   └── main.yml
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── README.md                # ← this file
├── tasks
│   └── main.yml
└── vars
    └── main.yml
```
