# Role: ado.platform.repos

Manages repository enable/disable operations on Red Hat-based systems.

The role supports:
- enabling repositories
- disabling repositories
- multiple execution methods (`rhsm_repository`, `yum_repository`, `file-edit`)
- optional cache cleanup and backup behavior

## Current Input Format and Planned Enhancement

Current implementation expects repository inputs as comma-separated strings.

Supported today:

```yaml
repos_to_enable: "repo1,repo2,repo3"
repos_to_disable: "repo4,repo5"
```

Planned enhancement (not implemented yet): support YAML/JSON list format.

```yaml
repos_to_enable:
  - repo1
  - repo2
```

## Requirements

- Target host OS family: `RedHat`
- Ansible with facts enabled (uses `ansible_os_family` and `ansible_pkg_mgr`)
- `community.general` collection for `rhsm_repository`
- Privileged access to manage repositories

## Workflow

`tasks/main.yml` dispatches based on `repos_action`:

- `repos_action: "enable"` -> runs `tasks/enable_repo.yml` (requires `repos_to_enable`)
- `repos_action: "disable"` -> runs `tasks/disable_repo.yml` (requires `repos_to_disable`)

Each action task:
1. validates required variables
2. validates OS compatibility (`RedHat`)
3. detects `subscription-manager` availability
4. applies selected/auto method
5. verifies repo state
6. optionally runs cache cleanup
7. prints summary output

## Variables

| Variable | Description | Required | Default |
| --- | --- | --- | --- |
| `repos_action` | Action to perform (`enable` or `disable`) | yes | none |
| `repos_to_enable` | Comma-separated repo IDs to enable | required for `enable` | none |
| `repos_to_disable` | Comma-separated repo IDs to disable | required for `disable` | none |
| `repos_enable_method` | Enable method: `rhsm_repository`, `yum_repository`, `file-edit` | no | auto |
| `repos_disable_method` | Disable method: `rhsm_repository`, `yum_repository`, `file-edit` | no | auto |
| `platform_repos_backup_files` | Backup repo files during `file-edit` method | no | `true` |
| `platform_repos_clean_cache` | Run package manager cache cleanup after action | no | `false` |

Compatibility note: legacy vars `repos_backup_files` and `repos_clean_cache` are still honored in task logic.

## Method Selection

When no method is explicitly set:

- if `subscription-manager` exists, role uses `rhsm_repository`
- otherwise role uses `yum_repository`

`file-edit` is only used when explicitly requested.

## Examples

### Enable repositories (auto method)

```yaml
- name: Enable repositories
  hosts: rhel_servers
  gather_facts: true
  vars:
    repos_action: "enable"
    repos_to_enable: "rhel-8-for-x86_64-appstream-rpms,rhel-8-for-x86_64-baseos-rpms"
  roles:
    - role: ado.platform.repos
```

### Disable repositories (auto method)

```yaml
- name: Disable repositories
  hosts: rhel_servers
  gather_facts: true
  vars:
    repos_action: "disable"
    repos_to_disable: "rhel-8-for-x86_64-appstream-rpms,rhel-8-for-x86_64-baseos-rpms"
  roles:
    - role: ado.platform.repos
```

### Enable with explicit method and cleanup

```yaml
- name: Enable repositories with RHSM
  hosts: rhel_servers
  gather_facts: true
  vars:
    repos_action: "enable"
    repos_to_enable: "rhel-8-for-x86_64-supplementary-rpms"
    repos_enable_method: "rhsm_repository"
    platform_repos_clean_cache: true
  roles:
    - role: ado.platform.repos
```

### Disable with file-edit fallback

```yaml
- name: Disable repositories with file editing
  hosts: rhel_servers
  gather_facts: true
  vars:
    repos_action: "disable"
    repos_to_disable: "epel,epel-modular"
    repos_disable_method: "file-edit"
    platform_repos_backup_files: true
  roles:
    - role: ado.platform.repos
```

## Testing

The role includes Molecule scenarios under `molecule/default` and `molecule/rhsm`.

## License

GPL-3.0-or-later
