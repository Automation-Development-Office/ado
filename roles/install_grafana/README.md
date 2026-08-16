# Role: infra.ado.install_grafana

Install **standalone Grafana** on RHEL via the official Grafana RPM repository
or an offline RPM.

## Requirements

- Ansible 2.16+
- Target: RHEL 8/9 (or compatible) with `become`
- Online: outbound HTTPS to `rpm.grafana.com`, **or**
- Airgap: `install_grafana_rpm_path` (Contoller path) / `install_grafana_rpm_url`

## Contoller / bootstrap

- Playbook seed:
  `bootstrap_generate_playbook_repo/files/playbooks/grafana/ado-install-grafana-standalone-bootstrap.yml`
- JT seed:
  `bootstrap_controller/files/job_templates/ado-install-grafana-standalone-bootstrap.jt.yml`
- Component keys: `grafana` (includes OpenShift operator JTs) and
  `grafana_standalone` (this role only)
- Prefer inventory host for the Grafana VM with a machine credential

## Example playbook

```yaml
- hosts: grafana_ado
  become: true
  roles:
    - role: infra.ado.install_grafana
      vars:
        install_grafana_hostname: grafana-ado.server.lab
        install_grafana_http_port: 3000
        install_grafana_admin_user: admin
        install_grafana_admin_password: "{{ vault_grafana_admin_password }}"
        # Airgap:
        # install_grafana_rpm_path: /var/tmp/grafana-*.rpm
```

## Defaults

| Variable | Default |
|----------|---------|
| `install_grafana_hostname` | `grafana-ado.server.lab` |
| `install_grafana_http_port` | `3000` |
| `install_grafana_admin_user` | `admin` |
| `install_grafana_admin_password` | `redhat123` |
| `install_grafana_skip_packages` | `false` |
| `install_grafana_rpm_path` / `install_grafana_rpm_url` | empty (online repo) |

The role writes `[server]` / `[security]` into `grafana.ini`, enables the
`grafana-server` systemd unit, and resets the admin password with
`grafana-cli` when available.
