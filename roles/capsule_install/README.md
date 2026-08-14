# Role: `capsule_install`

This Ansible role prepares and installs a Red Hat Satellite Capsule host on supported RHEL systems.

It currently implements preliminary validation in `tasks/preliminary_check.yml`, aligned with the `satellite_install` preliminary check workflow. Additional install tasks are planned.

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

## 📦 Role Variables

Defaults are defined in `defaults/main.yml`. Variables below are referenced by `tasks/preliminary_check.yml`.

### Preliminary check

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `capsule_install_os_version` | Capsule version referenced in OS validation messages | ✅ | `""` |
| `capsule_install_org_id` | Organization ID for Capsule registration | ✅ | unset |
| `capsule_install_activation_key` | Activation key for Capsule registration | ✅ | unset |
| `capsule_install_location` | Logical location/name for the Capsule deployment | ✅ | unset |
| `capsule_install_min_memory_size` | Minimum required memory in MB (`ansible_facts["memtotal_mb"]`) | ❌ | `12288` |
| `capsule_install_min_cpu_count` | Minimum required vCPU count (`ansible_facts["processor_vcpus"]`) | ❌ | `4` |

### Storage

| Variable | Default |
|----------|---------|
| `capsule_install_pulp_size` | `1500g` |
| `capsule_install_pgsql_size` | `150g` |
| `capsule_install_data_device` | `/dev` |
| `capsule_install_vg_name` | `capsule` |
| `capsule_install_data_disk_min_size` | `500` |
| `capsule_install_min_pulp_size` | `300` |
| `capsule_install_min_pgsql_size` | `20` |
| `capsule_install_req_dirs` | `/var/lib/pulp`, `/var/lib/pgsql` entries |

### Packages

| Variable | Default |
|----------|---------|
| `capsule_install_packages` | `satellite-capsule`, `chrony`, `sos`, `fapolicyd`, `vim`, `bash-completion`, `bind-utils` |
| `satellite_installer_scenario` | `capsule` |

### Administration

| Variable | Default |
|----------|---------|
| `capsule_install_admin_username` | `admin` |
| `capsule_install_admin_password` | unset |
| `satellite_fqdn` | unset |
| `capsule_install_sync_wait_time` | `86400` |

### Load balancing

| Variable | Default |
|----------|---------|
| `satellite_haproxy` | `false` |
| `satellite_loadbalancer_ports` | `80/tcp`, `443/tcp`, `8000/tcp`, `9090/tcp` |

### Installer options

| Variable | Default |
|----------|---------|
| `capsule_install_installer_options` | Standard Capsule installer flags (register, trusted-hosts, oauth, certs, remote execution) |
| `capsule_install_loadbalanced_options` | Capsule installer flags including load balancer CNAME/URLs |

See `defaults/main.yml` for default values and structure.

## 🚀 Role Usage

Define the Capsule installation configuration in your playbook or inventory using the variables above.

```yaml
- name: ADO | Install Capsule
  hosts: capsule_hosts
  become: true
  gather_facts: true
  vars:
    capsule_install_os_version: "6.19"
    capsule_install_org_id: "12345678"
    capsule_install_activation_key: "capsule-rhel9"
    capsule_install_location: AWS
  roles:
    - role: infra.ado.capsule_install
```

## 🔧 Tasks Overview

- **Main Task File** (`main.yml`):
  - Runs `preliminary_check.yml` for validation.
- **Preliminary Check** (`preliminary_check.yml`):
  - Validates RHEL version (9+), required inputs, and system resources.
  - Ensures `grubby` is installed, removes `ipv6.disable=1` kernel arguments, adds `ipv6.disable=0` if missing.
  - Sets SELinux to permissive and may trigger reboots via handlers.

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
    │   └── preliminary_check.yml
    ├── tests/
    │   └── inventory
    └── vars/
        └── main.yml
```
