# Role: `utilities_mount`

This Ansible role detects filesystem types and mounts block devices in a consistent, idempotent way for Linux systems.

It supports flexible mounting with optional automatic filesystem detection using `blkid`.

> **⚠️ Note:**
> This role requires root privileges for running `blkid` and mounting filesystems. Ensure your target hosts have the `ansible.posix` collection installed.

## ✅ Role Requirements

- Ansible >= 2.9
- Target hosts reachable by Ansible (privileged account or `become: true` required).
- The `ansible.posix` collection must be installed for the `mount` module.
- Block device must exist on the target system.

## 📦 Role Variables

| Variable                  | Description                                                     | Required | Default     |
|---------------------------|-----------------------------------------------------------------|----------|-------------|
| `mount_action`            | Mount action (`mounted`, `unmounted`, `absent`)                 | ✅       | N/A         |
| `mount_path`              | Mount point directory path (e.g., `/mnt/mydata`)                | ✅       | N/A         |
| `target_device`           | Path to the block device to mount (e.g., `/dev/sdb1`)           | ✅*      | N/A         |
| `mount_fstype`            | Explicitly specify the filesystem type (e.g., `xfs`, `ext4`)    | ✅**     | `undefined` |
| `mount_fstype_detection`  | Enable automatic filesystem type detection using `blkid`        | ❌       | `false`     |
| `mount_detected_fstype`   | Fact set by role containing detected filesystem type            | ❌       | `undefined` |

> **Notes:**
> \* `target_device` is required when `mount_action` is set to `mounted`.
> \*\* `mount_fstype` is required when mounting without `mount_fstype_detection` enabled.
> When `mount_fstype_detection` is `true`, the role auto-detects the filesystem type and sets `mount_detected_fstype`.

See `defaults/main.yml` and `vars/main.yml` for all available variables.

## 🚀 Usage

Define the mount configuration in your playbook or inventory using the variables above.

### Example 1: Mount a filesystem with automatic type detection
```yaml
- hosts: storage_servers
  become: true
  vars:
    mount_action: mounted
    target_device: /dev/sdb1
    mount_path: /mnt/data
    mount_fstype_detection: true
  roles:
    - role: infra.ado.utilities_mount
```

### Example 2: Mount a filesystem with explicit type
```yaml
- hosts: app_servers
  become: true
  vars:
    mount_action: mounted
    target_device: /dev/nvme1n1p1
    mount_path: /opt/app_data
    mount_fstype: xfs
  roles:
    - role: infra.ado.utilities_mount
```

### Example 3: Mount an EFS filesystem
```yaml
- hosts: web_servers
  become: true
  vars:
    mount_action: mounted
    target_device: fs-12345678.efs.us-east-1.amazonaws.com:/
    mount_path: /mnt/efs
    mount_fstype: efs
  roles:
    - role: infra.ado.utilities_mount
```

### Example 4: Unmount a filesystem
```yaml
- hosts: storage_servers
  become: true
  vars:
    mount_action: unmounted
    mount_path: /mnt/data
  roles:
    - role: infra.ado.utilities_mount
```

### Example 5: Remove a filesystem from fstab
```yaml
- hosts: storage_servers
  become: true
  vars:
    mount_action: absent
    mount_path: /mnt/data
  roles:
    - role: infra.ado.utilities_mount
```

## 🔧 Tasks Overview

- **Main Task File** (`main.yml`):
  - Validates required variables with assertions:
    - `mount_action` must be defined and one of: `mounted`, `unmounted`, `absent`
    - `mount_path` must be defined for all operations
    - `mount_fstype` must be defined when mounting without detection enabled
  - Conditionally imports filesystem detection tasks when `mount_fstype_detection` is `true`.
  - Conditionally imports mount, unmount, or remove tasks based on `mount_action`.
  - For `absent` action: unmounts filesystem first, then removes from fstab.
- **Filesystem Type Detection** (`get_fs_type.yml`):
  - Uses `blkid` command to detect filesystem types (when `mount_fstype_detection` is enabled).
  - Parses the `TYPE` field from `blkid` output using regex.
  - Sets `mount_detected_fstype` fact with detected type or `'none detected'`.
  - Displays detected filesystem type with verbosity level 1.
- **Mount Filesystem** (`mount_filesystem.yml`):
  - Sets `mount_fstype` fact from `mount_detected_fstype` if detection was enabled.
  - Uses `ansible.posix.mount` module for idempotent mounting operations.
  - Passes `mount_action` directly to the `state` parameter (typically `mounted`).
- **Unmount Filesystem** (`unmount_filesystem.yml`):
  - Uses `ansible.posix.mount` module to unmount filesystems.
  - Sets state to `unmounted` for the specified mount path.
- **Remove Mount from fstab** (`remove_mount_from_fstab.yml`):
  - Uses `ansible.posix.mount` module to remove mount entry from `/etc/fstab`.
  - Passes `mount_action` directly to the `state` parameter (typically `absent`).

## 🧪 Molecule

This role is tested with extension-level Molecule scenarios under `extensions/molecule/`.

Scenarios:

- `integration_utilities_mount_mount_auto_detect`
- `integration_utilities_mount_mount_explicit_fstype`
- `integration_utilities_mount_unmount_filesystem`
- `integration_utilities_mount_remove_from_fstab`

Shared playbooks are located in `extensions/molecule/utils/playbooks/` and include dedicated `prepare`, `converge`, `idempotence`, `verify`, and `destroy` flows for each scenario.

### Run scenarios locally

Run from the collection root using the same dependency bootstrap as CI:

```bash
cd /path/to/your/git/checkout/infra.ado
ansible-galaxy collection install . --force -p ~/.ansible/collections
ansible-galaxy collection install ansible.posix --force -p ~/.ansible/collections
export ANSIBLE_COLLECTIONS_PATH="$HOME/.ansible/collections:/usr/share/ansible/collections"
```

For fish shell:

```fish
set -gx ANSIBLE_COLLECTIONS_PATH "$HOME/.ansible/collections:/usr/share/ansible/collections"
```

Run scenarios from `extensions/`:

```bash
cd /path/to/your/git/checkout/infra.ado/extensions
molecule test -s integration_utilities_mount_mount_auto_detect
molecule test -s integration_utilities_mount_mount_explicit_fstype
molecule test -s integration_utilities_mount_unmount_filesystem
molecule test -s integration_utilities_mount_remove_from_fstab
```

### GitHub Actions manual runs

The `Ansible Collection CI/CD` workflow exposes each utils_mount scenario as a checkbox in `workflow_dispatch`.

- Checked scenarios are included in the Molecule matrix.
- Matrix jobs run in parallel.

## 📁 Structure

```
utilities_mount/
├── defaults/
│   └── main.yml
├── files/
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   ├── get_fs_type.yml
│   ├── main.yml
│   ├── mount_filesystem.yml
│   ├── remove_mount_from_fstab.yml
│   └── unmount_filesystem.yml
├── templates/
└── vars/
    └── main.yml
```

## License

GPL-3.0-or-later

## Author Information

Jeff Radabaugh (<jradabau@redhat.com>)
