# Role: infra.ado.bookstack_openshift

Deploy **BookStack** (internal Confluence-style docs) on OpenShift with MariaDB,
PVCs, Secrets, Service, Route, probes, and idempotent updates.

## Requirements

- Ansible 2.16+
- Collection: `kubernetes.core`
- OpenShift cluster credentials via `K8S_AUTH_*` / kubeconfig
- Ability to pull container images (or mirrored images for disconnected)

```yaml
# collections/requirements snippet
collections:
  - name: kubernetes.core
```

## What it creates

| Object | Name |
|--------|------|
| Namespace | `bookstack` (configurable) |
| Secret | `bookstack-db`, `bookstack-app` |
| PVC | `bookstack-mariadb`, `bookstack-data` |
| Deployment | `bookstack-mariadb`, `bookstack` |
| Service | `bookstack-mariadb`, `bookstack` |
| Route | `bookstack` (TLS edge + redirect) |

## Important defaults (OpenShift)

Default images that pull and run on this lab today:

- `docker.io/solidnerd/bookstack:24.12.1` (Apache listens on **8080**)
- `docker.io/library/mariadb:11` (probes use `mariadb-admin`; needs `bookstack_use_anyuid: true` on many clusters)

PVC mounts use an initContainer + subPaths so NFS volumes are writable by `www-data` (UID 33).

## Contoller / bootstrap

- Playbook template: `bootstrap_generate_playbook_repo/files/playbooks/docs/ado-deploy-bookstack-bootstrap.yml`
- JT seed: `bootstrap_controller/files/job_templates/ado-deploy-bookstack-bootstrap.jt.yml`
- Auth: load `vault_openshift.yml` + `vars_openshift.yml` and set `K8S_AUTH_*` from `host` / `token`
- Component registry key: `bookstack` in `bootstrap_resolve_component`

## Example playbook

```yaml
---
- name: Deploy BookStack to OpenShift
  hosts: localhost
  gather_facts: false
  environment:
    K8S_AUTH_HOST: "{{ host }}"
    K8S_AUTH_API_KEY: "{{ token }}"
    K8S_AUTH_VERIFY_SSL: "no"
  roles:
    - role: infra.ado.bookstack_openshift
      vars:
        bookstack_validate_certs: false
        bookstack_apps_domain: apps.ocp.prod.rhlab
        bookstack_route_host: bookstack.apps.ocp.prod.rhlab
        bookstack_storage_class: synology-nfs-csi
        bookstack_db_storage_class: synology-nfs-csi
        bookstack_use_anyuid: true
```

## Variables

See `defaults/main.yml`. Sensitive values:

- `bookstack_db_password` / `bookstack_db_root_password` / `bookstack_app_key`

If left empty, the role generates them **once** and stores them in Secrets (idempotent).

## Tags

`bookstack`, `bookstack_namespace`, `bookstack_database`, `bookstack_app`, `bookstack_route`, `bookstack_storage`

## Upgrade / backup

- Re-run the role to roll Deployments; PVCs and APP_KEY are preserved.
- Backup: snapshot/backup `bookstack-mariadb` + `bookstack-data` PVCs.
- Absent state removes Deployments/Services/Route/Secrets but **does not** delete PVCs unless `bookstack_purge_storage: true`.

## Future OIDC / Keycloak (RHBK)

Placeholders exist in defaults (`bookstack_oidc_*`). Not enabled by default.
