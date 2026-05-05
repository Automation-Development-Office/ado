---

# Role: `sat_reg`

This Ansible role automates the generation and execution of a Red Hat Satellite registration command using the `redhat.satellite.registration_command` module. It supports activation keys, lifecycle environments, and optional configuration for Insights and package updates.  
**Now supports both registration and deregistration actions.**

> **⚠️ Note:**  
> OS versions prior to RHEL 8 are no longer supported. Registration and deregistration tasks will not run on unsupported operating systems.

## ✅ Role Requirements

- Requires access to a Red Hat Satellite server.
- Ensure the `redhat.satellite` collection is installed.
- The target host must be reachable and have the necessary permissions to register with Satellite.
- Credentials (`sat_org_admin_account` and `sat_org_admin_account_password`) should be securely stored using Ansible Vault or AAP credentials.

## 📦 Role Variables

| Variable                        | Description                                                                | Required | Default |
|---------------------------------|----------------------------------------------------------------------------|----------|---------|
| `sat_org_admin_account`         | Satellite organization admin username                                      | ✅       | —       |
| `sat_org_admin_account_password`| Satellite organization admin password                                      | ✅       | —       |
| `sat_reg_activation_key_name`   | Activation key used for registration                                       | ✅       | —       |
| `sat_reg_satellite_org_name`    | Name of the Satellite organization                                         | ✅       | —       |
| `sat_reg_satellite_host`        | FQDN of the Satellite server                                               | ✅       | —       |
| `sat_reg_insights_enabled`      | Whether to enable Red Hat Insights during registration                     | ❌       | `false` |
| `sat_reg_update_packages`       | Whether to update packages during registration                             | ❌       | `false` |
| `sat_reg_validate_certs`        | Whether to validate SSL certificates                                       | ❌       | `true`  |
| `sat_reg_action`                | Action to perform: `"register"` or `"deregister"`                          | ✅       | `register` |
| `sat_reg_insecure`              | Whether to use insecure connection (skip SSL validation)                   | ❌       | `false` |
| `sat_reg_force_registration`    | Whether to force registration or not                                       | ❌       | `true`  |

## 🚀 Usage

Set `sat_reg_action` to `"register"` or `"deregister"` to control registration or deregistration.

## 🔧 Tasks Overview

- **Registration** (`reg_to_sat.yml`):
  - Gathers facts and checks OS support (RHEL 8+ only).
  - Generates registration command using `redhat.satellite.registration_command`.
  - Executes registration command.
  - Supports forcing registration, insecure registrations, and Insights

- **Deregistration** (`deregister_from_sat.yml`):
  - Gathers facts and checks OS support (RHEL 8+ only).
  - Unregisters system from subscription-manager.
  - Cleans local subscription-manager configs.
  - Removes Katello agent/consumer certs and custom yum repos.
  - Deletes the host record from Satellite via `redhat.satellite.host`.

- **Main Task File** (`main.yml`):
  - Imports registration or deregistration tasks based on `sat_reg_action`.

## 📁 Structure

```
sat_reg/
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
├── molecule/
│   └── default/
│       ├── .vault_pass
│       ├── converge.yml
│       ├── destroy.yml
│       ├── molecule.yml
│       ├── README.md
│       ├── TEST.md
│       ├── verify.yml
│       └── group_vars/
│           └── ...
├── files/
├── templates/
├── tests/
│   ├── inventory
│   └──
```