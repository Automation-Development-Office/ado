# Role: `capsule_install`

This Ansible role provides the skeleton for Red Hat Satellite Capsule installation workflows.

Current task files are scaffolding placeholders and intended to be implemented iteratively.

## Role Author

- Automation Development Office (automation-development-office@redhat.com)

## ✅ Role Requirements

- Ansible >= 2.9
- Target hosts: supported Red Hat Enterprise Linux (RHEL)
- Privileged access on the target host (`become: true`)

## 📦 Role Variables

Defaults are defined in `defaults/main.yml`.

### Core requirements

| Variable | Default |
|----------|---------|
| `capsule_install_min_cpu_count` | `4` |
| `capsule_install_min_memory_size` | `12288` |
| `capsule_install_data_disk_min_size` | `500` |
| `capsule_install_min_pulp_size` | `300` |
| `capsule_install_min_pgsql_size` | `20` |
| `capsule_install_pre_check` | `false` |

### Storage

| Variable | Default |
|----------|---------|
| `capsule_install_pulp_size` | `1500g` |
| `capsule_install_pgsql_size` | `150g` |
| `capsule_install_data_device` | `/dev` |
| `capsule_install_vg_name` | `capsule` |
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
| `capsule_install_rhn_org_id` | unset |
| `capsule_install_rhn_activation_key` | unset |
| `capsule_install_location` | unset |
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

## 🚀 Role Usage

```yaml
- name: ADO | Install Capsule
  hosts: capsule_hosts
  become: true
  gather_facts: true
  roles:
    - role: infra.ado.capsule_install
```

## 🔧 Tasks Overview

- Task implementation details in this role are currently in flux.
- Use the role directory as the source of truth for current task files and ownership.
- This README intentionally avoids listing individual task files to prevent drift.

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
    ├── templates/
    ├── tests/
    │   └── inventory
    └── vars/
        └── main.yml
```
