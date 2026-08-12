# Role: infra.ado.ocp_aap_hub_harden

Harden AAP Automation Hub against shared-Postgres `core_apiappstatus` LWLock
storms by pinning replicas, reducing workers, and installing a maintenance
CronJob.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core with `kubernetes.core` collection
- OpenShift/Kubernetes API access to the AAP namespace
- Existing `AnsibleAutomationPlatform` and `AutomationHub` custom resources
- Shared Postgres pod access for optional vacuum maintenance tasks

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_aap_hub_harden_namespace` | Namespace containing AAP CRs. Default `aap`. |
| `ocp_aap_hub_harden_aap_name` | `AnsibleAutomationPlatform` CR name. Default `aap`. |
| `ocp_aap_hub_harden_automationhub_name` | `AutomationHub` CR name. Default `aap-hub`. |
| `ocp_aap_hub_harden_api_replicas` | Hub API replica count. Default `1`. |
| `ocp_aap_hub_harden_content_replicas` | Hub content replica count. Default `1`. |
| `ocp_aap_hub_harden_gunicorn_api_workers` | Gunicorn API workers. Default `1`. |
| `ocp_aap_hub_harden_install_maintenance_cronjob` | Install stability CronJob. Default `true`. |
| `ocp_aap_hub_harden_cron_schedule` | CronJob schedule. Default `*/15 * * * *`. |

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_aap_hub_harden
      vars:
        ocp_aap_hub_harden_namespace: aap
        ocp_aap_hub_harden_aap_name: aap
```

See `ado-preflight-ui/docs/hub-recovery.md` for emergency recovery steps when Hub
status endpoints wedge shared Postgres.

## 🧪 Role Molecule Testing

This role targets live OpenShift clusters with AAP Hub installed. No Molecule
scenario is shipped; apply against a lab cluster and confirm Hub CR replica
counts and the `aap-hub-stability` CronJob.

```bash
ansible-playbook -i localhost, -c local playbooks/aap/ado-hub-harden-bootstrap.yml
```

## 📁 Role Structure

```text
roles/ocp_aap_hub_harden/
  README.md
  defaults/
  meta/
  tasks/
    main.yml
    install_cronjob.yml
```
