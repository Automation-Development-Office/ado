# Role: `platform_satellite_install`

This Ansible role prepares and installs a Red Hat Satellite host on supported RHEL systems.

It validates OS, CPU, memory, location, and Satellite version before install, supports a safe `pre_check` mode for validation-only runs, and can register the host to RHSM, patch it, prepare storage, install packages, and update DNS/firewall settings.

> **⚠️ Note:**
> This role requires root privileges for system modifications, package installation, and configuration changes. Ensure your target hosts are accessible with privileged access (`become: true`).

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

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `platform_satellite_install_pre_check` | When `true`, only run validation and host-readiness checks | ❌ | `false` |
| `platform_satellite_install_satellite_deployment_version` | Target Satellite version for validation and repository selection | ✅ | N/A |
| `platform_satellite_install_satellite_location` | Logical location/name for the Satellite deployment | ✅ | N/A |
| `platform_satellite_install_satellite_min_memory_size` | Minimum required memory in MB for preliminary checks | ✅ | N/A |
| `platform_satellite_install_satellite_min_cpu_count` | Minimum required vCPU count for preliminary checks | ✅ | N/A |
| `platform_satellite_install_satellite_rhn_connected` | Enable RHSM registration and subscription tasks | ❌ | N/A |
| `platform_satellite_install_satellite_rhn_org_id` | RHSM organization ID | ✅* | N/A |
| `platform_satellite_install_satellite_rhn_activation_key` | RHSM activation key | ✅* | N/A |
| `platform_satellite_install_satellite_rhn_repos` | RHSM repositories to enable during registration | ❌ | See `defaults/main.yml` |
| `platform_satellite_install_satellite_packages` | Packages to install, including `satellite`, `chrony`, etc. | ❌ | See `defaults/main.yml` |
| `platform_satellite_install_satellite_timezone` | Time zone configured before RHSM/subscription work | ❌ | N/A |
| `platform_satellite_install_satellite_selinux_state` | SELinux state applied during patching | ❌ | N/A |
| `platform_satellite_install_satellite_proxy_server` | Optional RHSM proxy hostname | ❌ | N/A |
| `platform_satellite_install_satellite_proxy_port` | Optional RHSM proxy port | ❌ | N/A |
| `platform_satellite_install_satellite_proxy_scheme` | Optional RHSM proxy scheme (`http` or `https`) | ❌ | N/A |
| `platform_satellite_install_satellite_vg_name` | Volume group name for Satellite storage layout | ❌ | N/A |
| `platform_satellite_install_satellite_req_dirs` | List of logical volumes and mount points for Satellite data paths | ❌ | N/A |
| `platform_satellite_install_satellite_data_disk_min_size` | Minimum disk size for auto-selecting data disk | ❌ | N/A |
| `platform_satellite_install_satellite_data_device_name` | Override for disk device when auto-discovery not desired | ❌ | N/A |
| `platform_satellite_install_satellite_data_device` | Base device path prefix (e.g., `/dev`) | ❌ | N/A |
| `platform_satellite_install_satellite_dns_device` | NetworkManager connection name for DNS updates | ❌ | N/A |
| `platform_satellite_install_satellite_dns_servers` | Optional list of DNS servers | ❌ | N/A |
| `platform_satellite_install_satellite_dns_search` | Optional DNS search domains | ❌ | N/A |

> **Notes:**
> \* Required when `manage_sat_install_satellite_rhn_connected: true`

See `defaults/main.yml` and `vars/main.yml` for all available variables.

## 🚀 Usage

Define the Satellite installation configuration in your playbook or inventory using the variables above.

### Example 1: Run validation checks only
```yaml
- hosts: satellite_hosts
  become: true
  vars:
    manage_sat_install_pre_check: true
    manage_sat_install_satellite_deployment_version: "6.16"
    manage_sat_install_satellite_location: lab-dc1
    manage_sat_install_satellite_rhn_connected: false
    manage_sat_install_satellite_min_memory_size: 20480
    manage_sat_install_satellite_min_cpu_count: 4
  roles:
    - role: infra.ado.manage_sat_install
```

### Example 2: Run a connected Satellite install
```yaml
- hosts: satellite_hosts
  become: true
  vars:
    manage_sat_install_pre_check: false
    manage_sat_install_satellite_deployment_version: "6.16"
    manage_sat_install_satellite_location: primary-dc
    manage_sat_install_satellite_rhn_connected: true
    manage_sat_install_satellite_rhn_org_id: "12345678"
    manage_sat_install_satellite_rhn_activation_key: "satellite-rhel9"
    manage_sat_install_satellite_timezone: America/New_York
    manage_sat_install_satellite_min_memory_size: 20480
    manage_sat_install_satellite_min_cpu_count: 4
    manage_sat_install_satellite_vg_name: satellite
    manage_sat_install_satellite_data_device: /dev
    manage_sat_install_satellite_data_disk_min_size: 500
    manage_sat_install_satellite_req_dirs:
      - lv_name: pulp
        lv_size: 250G
        mount_point: /var/lib/pulp
      - lv_name: postgres
        lv_size: 20G
        mount_point: /var/lib/pgsql
    manage_sat_install_satellite_dns_device: ens192
    manage_sat_install_satellite_dns_servers:
      - 10.0.0.10
      - 10.0.0.11
    manage_sat_install_satellite_dns_search:
      - example.com
  roles:
    - role: infra.ado.manage_sat_install
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

## 🧪 Molecule

This role includes a default Molecule scenario for testing.

The scenario runs the standard Molecule test sequence:

```text
dependency → create → converge → idempotence → verify → destroy
```

- Converge runs the role in safe `pre_check` mode
- Idempotence re-runs converge and expects no further changes
- Verify checks the README, pre-check completion marker, and required packages

### Run scenarios locally

Run from the collection root:

```bash
cd /path/to/cloned/ado
molecule test -s integration_manage_sat_install
```

## 👥 Author

- Automation Development Office (automation-development-office@redhat.com)

## 📁 Repository Layout (Role)

```text
roles/
└─ manage_sat_install/
   ├─ README.md
   ├─ defaults/
   │  └─ main.yml
   ├─ tasks/
   │  ├─ main.yml
   │  ├─ preliminary_check.yml
   │  ├─ rhsm_subscribe.yml
   │  ├─ patch.yml
   │  ├─ storage_config.yml
   │  ├─ install_packages.yml
   │  ├─ configure_firewall.yml
   │  ├─ prep-custom-certs.yml
   │  └─ dns_config.yml
   ├─ handlers/
   │  └─ main.yml
   ├─ meta/
   │  ├─ main.yml
   │  └─ argument_specs.yml
   ├─ templates/
   ├─ files/
   ├─ tests/
   │  └─ inventory
   └─ vars/
      └─ main.yml
```
