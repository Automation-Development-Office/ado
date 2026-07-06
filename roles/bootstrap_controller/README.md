# Role: infra.ado.bootstrap_controller

Generate and apply Ansible Automation Platform controller objects for an ADO
bootstrap repository.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- A reachable AAP controller or automation controller endpoint
- Controller credentials supplied through environment variables, inventory, or
  generated group variables
- Controller collections listed in `collections/requirements.yml`
- Generated controller configuration files under `configs/controller`,
  `configs/job_templates`, and `configs/workflows`

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `bootstrap_controller_enabled_objects` | Ordered list of controller object groups to manage. |
| `bootstrap_controller_generate_job_templates_from_manifest` | Enables rendering job template definitions from bundled bootstrap manifests. |
| `bootstrap_controller_organization` | Default organization used for generated controller objects. |
| `bootstrap_controller_inventory_name` | Default inventory assigned to generated job templates. |
| `bootstrap_controller_project_name` | Default project assigned to generated job templates. |
| `bootstrap_controller_execution_environment_name` | Default execution environment assigned to generated job templates. |
| `bootstrap_controller_controller_organizations` | Organization definitions to create or update. |
| `bootstrap_controller_controller_credentials` | Credential definitions to create or update. |
| `bootstrap_controller_controller_projects` | Project definitions to create or update. |
| `bootstrap_controller_controller_inventories` | Inventory definitions to create or update. |
| `bootstrap_controller_templates` | Job template definitions loaded from generated YAML. |
| `bootstrap_controller_workflow_job_templates` | Workflow job template definitions loaded from generated YAML. |

## 🚀 Role Usage

```yaml
- name: Apply generated ADO controller configuration
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.bootstrap_controller
      vars:
        bootstrap_controller_organization: ado-lab
        bootstrap_controller_project_name: ado-project
        bootstrap_controller_inventory_name: ado-inventory
```

## 🧪 Role Molecule Testing

This role is normally validated through the bootstrap scaffolding playbook and
targeted lint checks because it talks to a live AAP controller.

```bash
ansible-lint --offline roles/bootstrap_controller
yamllint roles/bootstrap_controller/tasks roles/bootstrap_controller/defaults
```

## 📁 Role Structure

```text
roles/bootstrap_controller/
  defaults/main.yml
  files/job_templates/
  files/workflows/
  tasks/
  templates/workflows/
  vars/main.yml
  README.md
```
