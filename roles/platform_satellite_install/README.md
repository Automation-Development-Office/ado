# Role: `platform_satellite_install`

This Ansible role prepares and installs a Red Hat Satellite host on supported RHEL systems.

It validates OS, CPU, memory, location, and Satellite version before install, supports a safe `pre_check` mode for validation-only runs, and can register the host to RHSM, patch it, prepare storage, install packages, and update DNS/firewall settings.

> **⚠️ Note:**
> This role requires root privileges for system modifications, package installation, and configuration changes. Ensure your target hosts are accessible with privileged access (`become: true`).

## Role Author

- Automation Development Office (automation-development-office@redhat.com)

## ✅ Role Requirements

- Ansible >= 2.9
- Target hosts: Supported Red Hat Enterprise Linux (RHEL 9 or later)
- Privileged access on the target host (`become: true`)
- Required collections:
  - `community.general`
  - `community.crypto`
  - `ansible.posix`
- RHSM activation key and organization ID (when `platform_satellite_install_satellite_rhn_connected: true`)
- Suitable additional disk for Satellite storage (optional, for automatic storage management)

## 📦 Role Variables

Variables below are referenced by the role task files under `tasks/`. Defaults are defined in `defaults/main.yml`.

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `platform_satellite_install_pre_check` | When `true`, only run `preliminary_check.yml` and skip all other tasks | ❌ | `false` |
| `platform_satellite_install_satellite_deployment_version` | Target Satellite version validated during preliminary checks and used in RHSM repo names | ✅ | `""` |
| `platform_satellite_install_satellite_location` | Logical location/name for the Satellite deployment | ✅ | `""` |
| `platform_satellite_install_satellite_min_memory_size` | Minimum required memory in MB (`ansible_facts["memtotal_mb"]`) | ❌ | `1024` |
| `platform_satellite_install_satellite_min_cpu_count` | Minimum required vCPU count and input to the Satellite tuning profile template | ❌ | `4` |
| `platform_satellite_install_satellite_rhn_connected` | When `true`, validate RHSM credentials during preliminary checks | ❌ | `false` |
| `platform_satellite_install_satellite_rhn_org_id` | RHSM organization ID used for host registration | ✅* | `""` |
| `platform_satellite_install_satellite_rhn_activation_key` | RHSM activation key used for host registration | ✅* | `""` |
| `platform_satellite_install_satellite_rhn_repos` | RHSM repository IDs enabled after registration | ❌ | See `defaults/main.yml` |
| `platform_satellite_install_satellite_timezone` | System timezone set before RHSM registration | ❌ | `"UTC"` |
| `platform_satellite_install_satellite_proxy_server` | Optional RHSM proxy hostname passed to `redhat_subscription` | ❌ | `""` |
| `platform_satellite_install_satellite_proxy_port` | Optional RHSM proxy port passed to `redhat_subscription` | ❌ | `""` |
| `platform_satellite_install_satellite_proxy_scheme` | Optional RHSM proxy scheme (`http` or `https`) passed to `redhat_subscription` | ❌ | `""` |
| `platform_satellite_install_satellite_selinux_state` | SELinux state applied after package updates | ❌ | `"enforcing"` |
| `platform_satellite_install_satellite_vg_name` | LVM volume group name for Satellite storage | ❌ | `"satellite"` |
| `platform_satellite_install_satellite_req_dirs` | List of logical volumes to create and mount; each item requires `lv_name`, `lv_size`, and `mount_point` | ❌† | `[]` |
| `platform_satellite_install_satellite_data_disk_min_size` | Minimum disk size used when auto-selecting an unpartitioned data disk | ❌ | `"10G"` |
| `platform_satellite_install_satellite_data_device_name` | Disk device basename override when auto-discovery finds multiple suitable disks | ❌ | `""` |
| `platform_satellite_install_satellite_data_device` | Base device path prefix joined with the selected disk (for example `/dev/sdb`) | ❌ | `"/dev"` |
| `platform_satellite_install_satellite_packages` | Package list installed before Satellite configuration | ❌ | See `defaults/main.yml` |
| `platform_satellite_install_satellite_dns_device` | NetworkManager connection name updated with DNS settings | ✅‡ | `""` |
| `platform_satellite_install_satellite_dns_servers` | DNS servers applied via NetworkManager and `/etc/resolv.conf` | ❌ | `[]` |
| `platform_satellite_install_satellite_dns_search` | DNS search domains applied via NetworkManager | ❌ | `[]` |
| `platform_satellite_install_satellite_size` | List of tuning tiers (`name`, `min_cpu`) used by `templates/tuning_profile.j2` to select the `satellite-installer --tuning` profile | ✅§ | Not defined in role defaults |

> **Notes:**
> \* Required when `platform_satellite_install_satellite_rhn_connected: true`
>
> † Required when configuring Satellite storage; each entry in `platform_satellite_install_satellite_req_dirs` must define `lv_name`, `lv_size`, and `mount_point`.
>
> ‡ Required when `platform_satellite_install_satellite_dns_servers` or `platform_satellite_install_satellite_dns_search` is set.
>
> § Required for a full install run (`platform_satellite_install_pre_check: false`) so `install_satellite.yml` can render the tuning profile.

See `defaults/main.yml` for default values and structure.

## 🚀 Role Usage

Define the Satellite installation configuration in your playbook or inventory using the variables above.

### Example 1: Run validation checks only
```yaml
- hosts: satellite_hosts
  become: true
  vars:
    platform_satellite_install_pre_check: true
    platform_satellite_install_satellite_deployment_version: "6.16"
    platform_satellite_install_satellite_location: lab-dc1
    platform_satellite_install_satellite_rhn_connected: false
    platform_satellite_install_satellite_min_memory_size: 20480
    platform_satellite_install_satellite_min_cpu_count: 4
  roles:
    - role: infra.ado.platform_satellite_install
```

### Example 2: Run a connected Satellite install
```yaml
- hosts: satellite_hosts
  become: true
  vars:
    platform_satellite_install_pre_check: false
    platform_satellite_install_satellite_deployment_version: "6.16"
    platform_satellite_install_satellite_location: primary-dc
    platform_satellite_install_satellite_rhn_connected: true
    platform_satellite_install_satellite_rhn_org_id: "12345678"
    platform_satellite_install_satellite_rhn_activation_key: "satellite-rhel9"
    platform_satellite_install_satellite_timezone: America/New_York
    platform_satellite_install_satellite_min_memory_size: 20480
    platform_satellite_install_satellite_min_cpu_count: 4
    platform_satellite_install_satellite_vg_name: satellite
    platform_satellite_install_satellite_data_device: /dev
    platform_satellite_install_satellite_data_disk_min_size: 500
    platform_satellite_install_satellite_req_dirs:
      - lv_name: pulp
        lv_size: 250G
        mount_point: /var/lib/pulp
      - lv_name: postgres
        lv_size: 20G
        mount_point: /var/lib/pgsql
    platform_satellite_install_satellite_dns_device: ens192
    platform_satellite_install_satellite_dns_servers:
      - 10.0.0.10
      - 10.0.0.11
    platform_satellite_install_satellite_dns_search:
      - example.com
  roles:
    - role: infra.ado.platform_satellite_install
```

## 🔧 Tasks Overview

- **Main Task File** (`main.yml`):
  - Always runs `preliminary_check.yml` first for validation.
  - When `pre_check: false`, continues with conditional task imports for RHSM subscription, patching, storage configuration, package installation, firewall configuration, certificate preparation, and DNS configuration.
- **Preliminary Check** (`preliminary_check.yml`):
  - Validates RHEL version (9+), required inputs, and system resources.
  - Ensures `grubby` is installed, removes `ipv6.disable=1` kernel arguments, adds `ipv6.disable=0` if missing.
  - Sets SELinux to permissive and may trigger reboots via handlers.
- **RHSM Subscribe** (`rhsm_subscribe.yml`):
  - Registers the host with RHSM using provided organization ID and activation key.
  - Enables specified repositories for Satellite installation.
- **Patch** (`patch.yml`):
  - Applies system patches and updates SELinux state.
- **Storage Config** (`storage_config.yml`):
  - Configures logical volumes and mount points for Satellite data directories.
  - Auto-detects suitable disks or uses explicit device specifications.
- **Install Packages** (`install_packages.yml`):
  - Installs Satellite and related packages from configured repositories.
- **Configure Firewall** (`configure_firewall.yml`):
  - Updates firewall rules for Satellite services.
- **Prep Custom Certificates** (`prep-custom-certs.yml`):
  - Prepares custom certificates using the `openssl.cnf.j2` template.
- **DNS Config** (`dns_config.yml`):
  - Updates DNS settings via NetworkManager and resolv.conf.

## 🧪 Role Molecule Testing

This role no longer includes a dedicated Molecule scenario or platform-specific Molecule playbooks.

> Molecule tests for `platform_satellite_install` have been removed from the repository.

## 📁 Role Structure

```text
roles/
└─ platform_satellite_install/
   ├─ README.md
   ├─ defaults/
   │  └─ main.yml
   ├─ handlers/
   │  └─ main.yml
   ├─ meta/
   │  ├─ argument_specs.yml
   │  └─ main.yml
   ├─ tasks/
   │  ├─ configure_firewall.yml
   │  ├─ dns_config.yml
   │  ├─ install_packages.yml
   │  ├─ install_satellite.yml
   │  ├─ main.yml
   │  ├─ patch.yml
   │  ├─ prep-custom-certs.yml
   │  ├─ preliminary_check.yml
   │  ├─ rhsm_subscribe.yml
   │  └─ storage_config.yml
   ├─ templates/
   │  ├─ openssl.cnf.j2
   │  └─ tuning_profile.j2
   ├─ tests/
   │  └─ inventory
   └─ vars/
      └─ main.yml
```
