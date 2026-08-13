# Role: infra.ado.ocp_aap_hub_harden

Pin AAP Automation Hub to a dedicated Postgres configuration secret, keep
replicas/workers conservative, and install a maintenance CronJob that vacuums
`core_apiappstatus` on the **dedicated** Hub database (not shared Controller PG).

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core with `kubernetes.core` collection
- OpenShift/Kubernetes API access to the AAP namespace
- Existing `AnsibleAutomationPlatform` and `AutomationHub` custom resources
- Dedicated Hub Postgres already provisioned and referenced by
  `external-hub-postgres-configuration` (or override vars below)

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `ocp_aap_hub_harden_namespace` | Namespace containing AAP CRs. Default `aap`. |
| `ocp_aap_hub_harden_aap_name` | `AnsibleAutomationPlatform` CR name. Default `aap`. |
| `ocp_aap_hub_harden_automationhub_name` | `AutomationHub` CR name. Default `aap-hub`. |
| `ocp_aap_hub_harden_postgres_pod` | Pod used for vacuum/LWLock cleanup. Default `aap-hub-dedicated-postgres-0`. |
| `ocp_aap_hub_harden_postgres_secret` | Unmanaged Hub DB secret. Default `external-hub-postgres-configuration`. |
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

See `ado-preflight-ui/docs/hub-recovery.md` for the permanent dedicated-DB
layout and emergency recovery (restart dedicated Hub Postgres only).

## 🧪 Role Molecule Testing

This role targets live OpenShift clusters with AAP Hub installed. No Molecule
scenario is shipped; apply against a lab cluster and confirm Hub CR replica
counts, dedicated DB secret pins, and the `aap-hub-stability` CronJob.

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
