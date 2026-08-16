# Role: infra.ado.install_gitlab

Install **standalone GitLab CE/EE** on RHEL via official Omnibus packages
(`packages.gitlab.com`) or an offline RPM.

Prefer **gitlab-ce** when no Enterprise license is available. Set
`install_gitlab_edition: ee` (package `gitlab-ee`) only when licensed.

## Requirements

- Ansible 2.16+
- Target: RHEL 8/9 (or compatible) with `become`
- Online: outbound HTTPS to `packages.gitlab.com`, **or**
- Airgap: `install_gitlab_rpm_path` (Contoller path) / `install_gitlab_rpm_url`

## Contoller / bootstrap

- Playbook seed:
  `bootstrap_generate_playbook_repo/files/playbooks/gitlab/ado-install-gitlab-standalone-bootstrap.yml`
- JT seed:
  `bootstrap_controller/files/job_templates/ado-install-gitlab-standalone-bootstrap.jt.yml`
- Component keys: `gitlab` (includes OpenShift operator JTs) and
  `gitlab_standalone` (this role only)
- Prefer inventory host for the GitLab VM with a machine credential

## Example playbook

```yaml
- hosts: gitlab_ado
  become: true
  roles:
    - role: infra.ado.install_gitlab
      vars:
        install_gitlab_hostname: gitlab-ado.server.lab
        install_gitlab_external_url: http://gitlab-ado.server.lab
        install_gitlab_root_password: "{{ vault_gitlab_root_password }}"
        # Optional EE:
        # install_gitlab_edition: ee
        # Airgap:
        # install_gitlab_rpm_path: /var/tmp/gitlab-ce-*.rpm
```

## Defaults

| Variable | Default |
|----------|---------|
| `install_gitlab_hostname` | `gitlab-ado.server.lab` |
| `install_gitlab_external_url` | derived (`http://` or `https://` if TLS PEMs set) |
| `install_gitlab_root_password` | `redhat123` |
| `install_gitlab_http_port` | `80` |
| `install_gitlab_https_port` | `443` |
| `install_gitlab_edition` | `ce` |
| `install_gitlab_skip_packages` | `false` |
| `install_gitlab_rpm_path` / `install_gitlab_rpm_url` | empty (online repo) |

Initial root password is written to `/etc/gitlab/gitlab.rb`
(`gitlab_rails['initial_root_password']`), matching the Omnibus
`GITLAB_ROOT_PASSWORD` first-boot pattern. Reconfigure via `gitlab-ctl`.

## TLS

Provide `install_gitlab_tls_crt` + `install_gitlab_tls_key` (or shared
`tls_crt` / `tls_key`) to enable HTTPS `external_url` and nginx cert paths
under `/etc/gitlab/ssl/`.
