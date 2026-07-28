# Role: infra.ado.aap_ocp_install

Installs Ansible Automation Platform 2.5 or 2.6 on OpenShift by validating the
ADO-supported inputs and delegating to the vendored
`infra.aap_utilities.aap_ocp_install` 3.5.0 implementation. Vendoring keeps
generated projects usable when disconnected from Automation Galaxy.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core 2.15 or later
- Python `kubernetes` 12.0 or later in the execution environment
- Collections: `kubernetes.core` and `redhat.openshift`
- An OpenShift token or username/password with permission to install operators
  and create AAP custom resources

## 📦 Role Variables

The wrapper intentionally uses the upstream `aap_ocp_install_*` interface.
The operator channel must begin with `stable-2.5` or `stable-2.6`. See the
upstream `infra.aap_utilities.aap_ocp_install` documentation for all nested
keys and manifest override options.

| Variable | Description |
|----------|-------------|
| `aap_ocp_install_namespace` | Namespace for the operator Subscription and AAP components. |
| `aap_ocp_install_create_namespace` | Whether to create `aap_ocp_install_namespace`. |
| `aap_ocp_install_connection` | OpenShift API connection (`host`, `api_key` or username/password). |
| `aap_ocp_install_operator` | Operator install settings including `channel`. |
| `aap_ocp_install_platform` | AAP 2.5+ platform CR settings (`instance_name`, `component_deployment`). |
| `aap_ocp_install_controller` | Controller component settings (`install`, overrides). |
| `aap_ocp_install_hub` | Hub component settings (`install`, storage, overrides). |
| `aap_ocp_install_eda` | EDA component settings (`install`, overrides). |
| `aap_ocp_install_lightspeed` | Optional Lightspeed enablement on AAP 2.5+. |

## 🚀 Role Usage

```yaml
---
- name: Install AAP 2.6 on OpenShift
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.aap_ocp_install
      vars:
        aap_ocp_install_namespace: aap
        aap_ocp_install_connection:
          host: https://api.example.com:6443
          api_key: "{{ vault_ocp_token }}"
          validate_certs: false
        aap_ocp_install_operator:
          channel: stable-2.6-cluster-scoped
        aap_ocp_install_platform:
          instance_name: aap
          component_deployment: unified
        aap_ocp_install_controller:
          install: true
        aap_ocp_install_hub:
          install: true
          storage_type: file
          file_storage_storage_class: ocs-storagecluster-cephfs
          file_storage_size: 20Gi
        aap_ocp_install_eda:
          install: true
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

```bash
cd roles/aap_ocp_install
molecule test
```

## 📁 Role Structure

```text
roles/aap_ocp_install/
  README.md
  defaults/
  meta/
  tasks/
```
