# Role: ado.utilities.utilities_services_management

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
|---------|-------------|
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
    - role: ado.utilities.utilities_services_management
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
    - role: ado.utilities.utilities_services_management
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
    - role: ado.utilities.utilities_services_management
```

---

## Behavior Notes

- Uses `ansible.builtin.service_facts` to discover available services.
- For each name in `service_names`, the role manages it **only if** the service (or `${name}.service`) exists in `ansible_facts.services`.
- On non‑systemd hosts (or where `service_facts` is unavailable), the role performs no changes.
- Operations are idempotent; repeated runs won’t introduce changes unless service state drifts.

---

## Molecule

A default Molecule scenario is included for this role. It runs:

```
dependency → lint → syntax → create → converge → idempotence → destroy → verify
```

> Tip: If testing on images with self‑managed init, ensure systemd is running so `service_facts` can populate.

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
├── molecule
│   └── default
│       ├── converge.yml
│       ├── destroy.yml
│       ├── group_vars
│       │   └── all
│       │       └── vault.yml
│       ├── molecule.yml
│       ├── README.md
│       ├── TEST.md
│       └── verify.yml
├── README.md                # ← this file
├── tasks
│   └── main.yml
├── tests
│   ├── inventory
│   └── test.yml
└── vars
    └── main.yml
```
