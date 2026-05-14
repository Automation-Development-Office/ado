# Role: ado.platform.patching

This role provides comprehensive patching functionality for Red Hat Enterprise Linux (RHEL) servers. It handles package updates, kernel management, IPA client updates, system reboots, and provides detailed patching statistics. The role includes safety checks for supported RHEL versions and ELS (Extended Life Cycle Support) requirements for RHEL 7 systems.

## ✅ Role Requirements

- Red Hat Enterprise Linux 7, 8, or 9 (RHEL 6 is not supported)
- For RHEL 7: Extended Life Cycle Support (ELS) repositories must be configured
- SSH access with sudo privileges
- The following collections installed:
  - `ansible.builtin`
- Package management utilities (dnf/yum) available on target systems

## 📦 Role Variables

| Variable                    | Description                                                | Required | Default |
|-----------------------------|------------------------------------------------------------|----------|---------|
| `platform_patching_package_cleanup`  | Whether to clean up old kernels from /boot        | ❌       | `false` |
| `platform_patching_versions`         | Version specification for package updates         | ❌       | `latest`|
| `platform_patching_update_cache`     | Whether to update package cache before patching   | ❌       | `false` |
| `platform_patching_exclude_list`     | List of packages to exclude from updates          | ❌       | `[]`    |
| `platform_patching_disable_repos`    | List of repositories to disable during patching   | ❌       | `[]`    |
| `platform_patching_skip_broken`      | Whether to skip broken dependencies               | ❌       | `false` |
| `platform_patching_package_list`     | Specific list of packages to update (optional)    | ❌       | —       |

### Optional Variables (Commented in defaults)
| Variable                    | Description                                                | Default |
|-----------------------------|------------------------------------------------------------|---------|
| `platform_patching_check_mountpoints`| Whether to check server mountpoints before patching| `true`  |
| `platform_patching_reboot`           | Whether to reboot servers after patching           | `false` |

---

## 📘 Example Usage

### Basic Patching (No Reboot)
```yaml
- name: Patch RHEL servers
  hosts: rhel_servers
  gather_facts: true
  vars:
    platform_patching_update_cache: true
    platform_patching_package_cleanup: true
  roles:
    - role: infra.ado.platform_patching
```

### Patching with Forced Restart
```yaml
- name: Patch and restart RHEL servers
  hosts: rhel_servers
  gather_facts: true
  vars:
    platform_patching_reboot: true
    platform_patching_update_cache: true
    platform_patching_package_cleanup: true
  roles:
    - role: infra.ado.platform_patching
```

### Selective Package Patching
```yaml
- name: Update specific packages
  hosts: rhel_servers
  gather_facts: true
  vars:
    platform_patching_package_list:
      - httpd
      - nginx
      - openssh
    platform_patching_versions: latest
    platform_patching_exclude_list: []
  roles:
    - role: infra.ado.platform_patching
```

### Advanced Patching Configuration
```yaml
- name: Advanced patching with custom settings
  hosts: rhel_servers
  gather_facts: true
  vars:
    patching_reboot: true
    patching_update_cache: true
    patching_package_cleanup: true
    patching_exclude_list:
      - kernel-debug
      - custom-app
    patching_disable_repos:
      - epel-testing
    patching_skip_broken: true
  roles:
    - role: infra.ado.platform_patching
```

## 🔍 Role Features

### Safety Checks
- **RHEL Version Validation**: Ensures only RHEL 7, 8, or 9 systems are patched
- **ELS Repository Check**: Validates ELS repositories are present for RHEL 7 systems
- **Pre-patch Statistics**: Captures kernel version and system uptime before patching

### Patching Process
1. **Repository Information**: Gathers information about configured repositories
2. **Package Information**: Collects data about available package updates
3. **Cache Management**: Optionally updates package cache
4. **Kernel Cleanup**: Removes old kernels if enabled
5. **IPA Client Updates**: Updates IPA client packages separately if enabled
6. **Package Updates**: Updates remaining packages (excluding specified packages)
7. **Conditional Reboot**: Reboots system if forced restart is enabled and changes occurred

### Post-Patch Activities
- **Statistics Collection**: Gathers post-patch kernel version and uptime
- **Reboot Monitoring**: Tracks reboot time and waits for system availability
- **Fact Refresh**: Re-gathers Ansible facts after reboot
- **Reporting**: Displays comprehensive before/after patching statistics

## 📊 Patching Statistics

The role provides detailed statistics including:
- Pre/post-patch system uptime (in days)
- Pre/post-patch kernel versions
- Number of available updates
- Reboot duration (when applicable)
- Package update details (in debug mode)

**Structure:**
```
patching/
├── defaults/main.yml
├── vars/main.yml
├── tasks/
│   ├── main.yml
│   ├── patch.yml
│   ├── reboot.yml
│   ├── package_facts.yml
│   ├── repo_facts.yml
│   ├── recon.yml
│   ├── pre_patch_mail.yml
│   ├── pre_auto_patch_mail.yml
│   └── post_patch_mail.yml
├── templates/
├── handlers/main.yml
├── files/
├── tests/
│   ├── inventory
│   └── test.yml
└── README.md
```
