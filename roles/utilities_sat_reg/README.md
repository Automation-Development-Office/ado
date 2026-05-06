---

# Role: `utilities_sat_reg`

This Ansible role automates registration and deregistration of hosts with Red Hat Satellite using the `redhat.satellite.registration_command` and `redhat.satellite.host` modules. It supports activation keys, lifecycle environments, Insights, package updates, and robust cleanup.

> **Note:** OS versions prior to RHEL 8 are not supported. Tasks will not run on unsupported operating systems.

## ✅ Requirements
- Red Hat Satellite server access
- `redhat.satellite` collection installed
- Target host must be reachable and have permissions to register/deregister
- Credentials (`sat_org_admin_account` and `sat_org_admin_account_password`) should be securely stored (e.g., Ansible Vault)

## 📦 Role Variables
| Variable                              | Description                                                                | Required | Default     |
|----------------------------------------|----------------------------------------------------------------------------|----------|-------------|
| `sat_org_admin_account`                | Satellite organization admin username                                      | ✅       | —           |
| `sat_org_admin_account_password`       | Satellite organization admin password                                      | ✅       | —           |
| `sat_reg_activation_key_name`          | Activation key used for registration                                       | ✅       | —           |
| `sat_reg_satellite_org_name`           | Name of the Satellite organization                                         | ✅       | —           |
| `sat_reg_satellite_host`               | FQDN of the Satellite server                                               | ✅       | —           |
| `sat_reg_insights_enabled`             | Enable Red Hat Insights during registration                                | ❌       | `false`     |
| `sat_reg_update_packages`              | Update packages during registration                                        | ❌       | `false`     |
| `sat_reg_validate_certs`               | Validate SSL certificates                                                  | ❌       | `true`      |
| `sat_reg_action`                       | Action: `register` or `deregister`                                         | ✅       | `register`  |
| `sat_reg_insecure`                     | Use insecure connection (skip SSL validation)                              | ❌       | `false`     |
| `sat_reg_force_registration`           | Force registration                                                        | ❌       | `true`      |

## 🚀 Usage Example
```yaml
- hosts: all
  roles:
    - role: utilities_sat_reg
      vars:
        sat_org_admin_account: "admin"
        sat_org_admin_account_password: "{{ vault_sat_password }}"
        sat_reg_activation_key_name: "my-key"
        sat_reg_satellite_org_name: "MyOrg"
        sat_reg_satellite_host: "satellite.example.com"
        sat_reg_action: "register"  # or "deregister"
```

## 🔧 Tasks Overview
- **Registration** (`reg_to_sat.yml`):
  - Gathers facts and checks OS support (RHEL 8+ only)
  - Generates registration command using `redhat.satellite.registration_command`
  - Executes registration command
  - Supports force/insecure/Insights options
  - Registered variables: `utilities_sat_reg_command`, `utilities_sat_reg_script_result`
- **Deregistration** (`deregister_from_sat.yml`):
  - Gathers facts and checks OS support (RHEL 8+ only)
  - Unregisters from subscription-manager
  - Cleans configs, removes certs/repos, deletes host from Satellite
  - Registered variables: `utilities_sat_reg_unregister_result`, `utilities_sat_reg_clean_result`
- **Main Task File** (`main.yml`):
  - Imports registration or deregistration tasks based on `sat_reg_action`

## 🧪 Molecule Testing
- Scenario: `integration_utilities_sat_reg`
- Playbooks:
  - Converge: `../utils/playbooks/utilities_sat_reg_converge.yml`
  - Destroy: `../utils/playbooks/utilities_sat_reg_destroy.yml`
  - Verify:  `../utils/playbooks/utilities_sat_reg_verify.yml`

## 📁 Structure
```
utilities_sat_reg/
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
- All variable names and registered variables use the `utilities_sat_reg_` prefix for lint compliance.
#- Molecule scenarios reference playbooks using correct relative paths.
- Molecule testing temporarily removed due to github restrictions. Remove this tag once it's been added back.
- Example usage and documentation are up to date with current role structure and naming.
- For best security, use Ansible Vault for sensitive variables.
- Ensure the `redhat.satellite` collection is installed on your control node or inside your execution environment.