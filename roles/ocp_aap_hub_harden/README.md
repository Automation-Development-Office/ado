# Role: infra.ado.ocp_aap_hub_harden

Hardens AAP Automation Hub against shared-Postgres `core_apiappstatus` LWLock storms.

## What it does
- Pins Hub replicas to 1/1/1/1 on the parent `AnsibleAutomationPlatform` CR
- Sets `gunicorn_api_workers` / content workers to 1 and raises timeouts on `AutomationHub`
- Installs CronJob `aap-hub-stability` (vacuum + long LWLock kill + CR re-pin)

## Example
```yaml
- hosts: localhost
  roles:
    - role: infra.ado.ocp_aap_hub_harden
```

See `ado-preflight-ui/docs/hub-recovery.md` for emergency recovery.
