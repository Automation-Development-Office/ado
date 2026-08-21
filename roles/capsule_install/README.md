# Role: `capsule_install`

This Ansible role prepares and installs a Red Hat Satellite Capsule host on supported RHEL systems.

It validates OS, CPU, memory, location, and Capsule version before install, supports a safe `pre_check` mode for validation-only runs, and can register the Capsule host to Satellite using a generated registration command.

> **⚠️ Note:**
> This role requires root privileges for system modifications, package installation, and configuration changes. Ensure your target hosts are accessible with privileged access (`become: true`).

## Role Author

- Automation Development Office (automation-development-office@redhat.com)

## ✅ Role Requirements

- Ansible >= 2.9
- Target hosts: Supported Red Hat Enterprise Linux (RHEL 9 or later)
- Privileged access on the target host (`become: true`)
- Required collections:
  - `ansible.posix`
  - `community.general`
  - `redhat.satellite`
- Upstream Satellite server FQDN, organization ID, activation key, and admin credentials for Capsule registration

## 📦 Role Variables

Variables below are referenced by the role task files under `tasks/`. Defaults are defined in `defaults/main.yml`.

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `capsule_install_pre_check` | When `true`, only run the preliminary validation tasks and skip the remaining install tasks | ❌ | `false` |
| `capsule_install_os_version` | RHEL major version referenced in OS validation messages | ❌ | `"9"` |
| `capsule_install_deployment_version` | Target Capsule version used in RHSM repo names | ❌ | `"6.19"` |
| `capsule_install_location` | Logical location/name for the Capsule deployment | ✅ | `""` |
| `capsule_install_min_memory_size` | Minimum required memory in MB (`ansible_facts["memtotal_mb"]`) | ❌ | `12288` |
| `capsule_install_min_cpu_count` | Minimum required vCPU count (`ansible_facts["processor_vcpus"]`) | ❌ | `4` |
| `capsule_install_org_id` | Organization ID used for Capsule registration | ✅ | unset |
| `capsule_install_activation_key` | Activation key used for Capsule registration | ✅ | unset |
| `capsule_install_satellite_fqdn` | FQDN of the upstream Satellite server | ✅* | unset |
| `capsule_install_admin_username` | Satellite admin username used to generate the registration command | ❌ | `"admin"` |
| `capsule_install_admin_password` | Satellite admin password used to generate the registration command | ✅* | unset |
| `capsule_install_timezone` | System timezone set before registration | ❌ | `"UTC"` |
| `capsule_install_rhn_repos` | RHSM repository IDs enabled after registration | ❌ | See `defaults/main.yml` |
| `capsule_install_scenario` | Satellite installer scenario for Capsule deployment | ❌ | `"capsule"` |
| `capsule_install_vg_name` | LVM volume group name for Capsule storage | ❌ | `"capsule"` |
| `capsule_install_req_dirs` | List of logical volumes to create and mount; each item requires `lv_name`, `lv_size`, and `mount_point` | ❌ | `/var/lib/pulp` and `/var/lib/pgsql` defaults |
| `capsule_install_data_disk_min_size` | Minimum disk size in GB used when validating storage requirements | ❌ | `500` |
| `capsule_install_data_device` | Base device path prefix joined with the selected disk | ❌ | `"/dev"` |
| `capsule_install_packages` | Package list installed for Capsule deployment | ❌ | See `defaults/main.yml` |
| `capsule_install_satellite_haproxy` | Enable load-balanced Capsule registration settings | ❌ | `false` |
| `capsule_install_satellite_loadbalancer_ports` | Firewall/service ports used by load-balanced deployments | ❌ | See `defaults/main.yml` |
| `capsule_install_installer_options` | Installer flags for standard Capsule deployment | ❌ | See `defaults/main.yml` |
| `capsule_install_loadbalanced_options` | Installer flags for load-balanced Capsule deployment | ❌ | See `defaults/main.yml` |
| `capsule_install_sync_wait_time` | Maximum wait time for synchronization operations | ❌ | `86400` |

> **Notes:**
> \* Required when `capsule_install_pre_check: false` so `rhsm_subscribe.yml` can register the Capsule host.

See `defaults/main.yml` for default values and structure.

## 🚀 Role Usage

Define the Capsule installation configuration in your playbook or inventory using the variables above.

### Example 1: Run validation checks only

```yaml
- name: ADO | Validate Capsule host
  hosts: capsule_hosts
  become: true
  gather_facts: true
  vars:
    capsule_install_pre_check: true
    capsule_install_os_version: "9"
    capsule_install_org_id: "12345678"
    capsule_install_activation_key: "capsule-rhel9"
    capsule_install_location: AWS
  roles:
    - role: infra.ado.capsule_install
```

### Example 2: Run preliminary check and Capsule registration

```yaml
- name: ADO | Install Capsule
  hosts: capsule_hosts
  become: true
  gather_facts: true
  vars:
    capsule_install_pre_check: false
    capsule_install_os_version: "9"
    capsule_install_deployment_version: "6.19"
    capsule_install_org_id: "12345678"
    capsule_install_activation_key: "capsule-rhel9"
    capsule_install_location: AWS
    capsule_install_satellite_fqdn: satellite.example.com
    capsule_install_admin_password: "StrongAdminPassword123!"
  roles:
    - role: infra.ado.capsule_install
```

## 🧪 Role Molecule Testing

This role does not currently include a dedicated Molecule scenario or platform-specific Molecule playbooks.

> Molecule tests for `capsule_install` have not been added to the repository.

## 🔧 Tasks Overview

- **Main Task File** (`main.yml`):
  - Always runs `preliminary_check.yml` first for validation.
  - When `capsule_install_pre_check: false`, continues with `rhsm_subscribe.yml`.
- **Preliminary Check** (`preliminary_check.yml`):
  - Validates RHEL version (9+), required inputs, and system resources.
  - Ensures `grubby` is installed, removes `ipv6.disable=1` kernel arguments, adds `ipv6.disable=0` if missing.
  - Sets SELinux to permissive and may trigger reboots via handlers.
- **RHSM Subscribe** (`rhsm_subscribe.yml`):
  - Sets the system timezone and restarts `crond`.
  - Removes non-Red Hat repository files when the Capsule is not already registered.
  - Generates a Satellite registration command with `redhat.satellite.registration_command`.
  - Registers the host and enables repositories from `capsule_install_rhn_repos`.

## 🔄 Handlers

- **Reboot node** (`reboot system`):
  - Reboots the host after kernel argument or SELinux changes, with a 600-second timeout.

## 📁 Role Structure

```text
roles/
└── capsule_install/
    ├── README.md
    ├── defaults/
    │   └── main.yml
    ├── handlers/
    │   └── main.yml
    ├── meta/
    │   ├── argument_specs.yml
    │   └── main.yml
    ├── tasks/
    │   ├── main.yml
    │   ├── preliminary_check.yml
    │   └── rhsm_subscribe.yml
    ├── tests/
    │   └── inventory
    └── vars/
        └── main.yml
```
