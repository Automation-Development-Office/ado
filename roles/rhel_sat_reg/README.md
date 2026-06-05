---

# Role: `rhel_sat_reg`

This Ansible role automates registration and deregistration of hosts with Red Hat Satellite using the `redhat.satellite.registration_command` and `redhat.satellite.host` modules. It supports activation keys, lifecycle environments, Insights, package updates, and robust cleanup.

> **Note:** OS versions prior to RHEL 8 are not supported. Tasks will not run on unsupported operating systems.

## ✅ Requirements
- Red Hat Satellite server access
- `redhat.satellite` collection installed
- Target host must be reachable and have permissions to register/deregister
- Credentials (`rhel_sat_reg_org_admin_account` and `rhel_sat_reg_org_admin_account_password`) should be securely stored (e.g., Ansible Vault)

## 📦 Role Variables
| Variable                              | Description                                                                | Required | Default     |
|----------------------------------------|----------------------------------------------------------------------------|----------|-------------|
| `rhel_sat_reg_org_admin_account`                | Satellite organization admin username                                      | ✅       | —           |
| `rhel_sat_reg_org_admin_account_password`       | Satellite organization admin password                                      | ✅       | —           |
| `rhel_sat_reg_activation_key_name`          | Activation key used for registration                                       | ✅       | —           |
| `rhel_sat_reg_satellite_org_name`           | Name of the Satellite organization                                         | ✅       | —           |
| `rhel_sat_reg_satellite_host`               | FQDN of the Satellite server                                               | ✅       | —           |
| `rhel_sat_reg_insights_enabled`             | Enable Red Hat Insights during registration                                | ❌       | `false`     |
| `rhel_sat_reg_update_packages`              | Update packages during registration                                        | ❌       | `false`     |
| `rhel_sat_reg_validate_certs`               | Validate SSL certificates                                                  | ❌       | `true`      |
| `rhel_sat_reg_action`                       | Action: `register` or `deregister`                                         | ✅       | `register`  |
| `rhel_sat_reg_insecure`                     | Use insecure connection (skip SSL validation)                              | ❌       | `false`     |
| `rhel_sat_reg_force_registration`           | Force registration                                                        | ❌       | `true`      |

## 🚀 Usage Example
```yaml
- hosts: all
  roles:
    - role: infra.ado.rhel_sat_reg
      vars:
        rhel_sat_reg_org_admin_account: "admin"
        rhel_sat_reg_org_admin_account_password: "{{ vault_sat_password }}"
        rhel_sat_reg_activation_key_name: "my-key"
        rhel_sat_reg_satellite_org_name: "MyOrg"
        rhel_sat_reg_satellite_host: "satellite.example.com"
        rhel_sat_reg_action: "register"  # or "deregister"
```

## 🔧 Tasks Overview
- **Registration** (`reg_to_sat.yml`):
  - Gathers facts and checks OS support (RHEL 8+ only)
  - Generates registration command using `redhat.satellite.registration_command`
  - Executes registration command
  - Supports force/insecure/Insights options
  - Registered variables: `rhel_sat_reg_command`, `rhel_sat_reg_script_result`
- **Deregistration** (`deregister_from_sat.yml`):
  - Gathers facts and checks OS support (RHEL 8+ only)
  - Unregisters from subscription-manager
  - Cleans configs, removes certs/repos, deletes host from Satellite
  - Registered variables: `rhel_sat_reg_unregister_result`, `rhel_sat_reg_clean_result`
- **Main Task File** (`main.yml`):
  - Imports registration or deregistration tasks based on `rhel_sat_reg_action`

## 🧪 Molecule Testing
This role currently does not include an active dedicated Molecule scenario in the repository.

## 📁 Structure
```
rhel_sat_reg/
├── defaults/
│   └── main.yml
├── vars/
│   └── main.yml
├── tasks/
│   ├── main.yml
│   ├── reg_to_sat.yml
│   └── deregister_from_sat.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── files/
├── templates/
├── tests/
│   ├── inventory
│   └── ...
```

## 📝 Notes & Optimization
- All variable names and registered variables use the `rhel_sat_reg_` prefix for lint compliance.
#- Molecule scenarios reference playbooks using correct relative paths.
- Molecule testing temporarily removed due to github restrictions. Remove this tag once it's been added back.
- Example usage and documentation are up to date with current role structure and naming.
- For best security, use Ansible Vault for sensitive variables.
- Ensure the `redhat.satellite` collection is installed on your control node or inside your execution environment.