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
| `bootstrap_controller_aap_connectivity_check_enabled` | Checks AAP controller API connectivity and authentication before applying controller objects. Defaults to `true`. |
| `bootstrap_controller_aap_smoke_test_enabled` | Launches a harmless AAP job template before applying controller objects. Defaults to `true`. |
| `bootstrap_controller_aap_smoke_test_job_template` | Job template used for the AAP smoke test. Defaults to `Demo Job Template`. |
| `bootstrap_controller_organization` | Default organization used for generated controller objects. |
| `bootstrap_controller_inventory_name` | Default inventory assigned to generated job templates. |
| `bootstrap_controller_local_inventory_name` | Local bootstrap inventory name. Defaults to `bootstrap_controller_inventory_name`. |
| `bootstrap_controller_rhel_inventory_name` | RHEL managed-host inventory used by RHEL patching, Satellite registration, IDM client, compliance, and STIG job templates. |
| `bootstrap_controller_idm_inventory_name` | IDM server inventory used by IDM server, replica, DNS, topology, sudo, and server settings job templates. |
| `bootstrap_controller_satellite_inventory_name` | Satellite server inventory used by Satellite install, configure, and content-view job templates. |
| `bootstrap_controller_project_name` | Default project assigned to generated job templates. |
| `bootstrap_controller_execution_environment_name` | Default execution environment assigned to generated job templates. |
| `bootstrap_controller_controller_organizations` | Organization definitions to create or update. |
| `bootstrap_controller_controller_credentials` | Credential definitions to create or update. |
| `bootstrap_controller_controller_projects` | Project definitions to create or update. |
| `bootstrap_controller_controller_inventories` | Inventory definitions to create or update. |
| `bootstrap_controller_templates` | Job template definitions loaded from generated YAML. |
| `bootstrap_controller_workflow_job_templates` | Workflow job template definitions loaded from generated YAML. |
| `bootstrap_controller_controller_labels` | Controller labels to create. Generated runs include an organization label such as `ADO` alongside component labels such as `ADO | rhel`. |

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

Generated workflows use simplified workflow nodes so the AAP configuration
collection creates both the workflow template and its links reliably.
The apply path maps generated workflow files to `controller_workflows`, which
is the dispatcher variable used by `infra.aap_configuration` for workflow job
templates.

Generated patching workflows are created when RHEL, Satellite, and IDM are
selected. The workflow chain is `Register Host to Satellite` ->
`RHEL Patch Host` -> `IdM Manage Client`.

Generated RHEL bootstrap workflows are created when the selected component set
includes RHEL, Satellite, IDM, compliance, and STIG. The workflow chain is
`Register Host to Satellite` -> `RHEL Patch Host` -> `IdM Manage Client` ->
`RHEL Compliance` -> `RHEL STIG Hardening`.

Generated Satellite workflows are created when Satellite is selected and run
`Satellite Server Install` -> `Satellite Server Configure`.

Generated OpenShift workflows are created when OpenShift is selected. The
workflow starts with `Create Admin HTPasswd User`, then runs selected
cert-manager and console banner jobs, and fans out to selected platform
services such as RHBK, Grafana, GitLab, Pega, Kafka, AAP, ECK, GitOps, 389ds,
OADP, Quay, ACS, and ACM. Workflow nodes are pruned when their job templates
were not generated, so single-app and partial OpenShift selections remain
valid.

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
