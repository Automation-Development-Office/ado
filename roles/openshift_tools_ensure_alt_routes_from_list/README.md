# Role: openshift_tools_ensure_alt_routes_from_list

Ensure alternate OpenShift routes exist for each route definition in a caller-provided list.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.

---

## Variables

| Variable | Description |
|---------|-------------|
| `ensure_alt_routes_from_list_routes` | List of route definitions to process. Required. |
| `ensure_alt_routes_from_list_default_tls_termination` | Default TLS termination used when a route item does not override it. |
| `route_labels` | Optional labels applied to generated route resources. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_tools_ensure_alt_routes_from_list
      vars:
        ensure_alt_routes_from_list_routes:
          - namespace: grafana
            route_name: grafana
            route_name_alt: grafana-alt
            route_host_alt: grafana-alt.apps.example.com
            backend_svc: grafana-service
            backend_port: https
```

---

## Behavior Notes

- Processes each route entry and creates or updates the alternate route when needed.
- This role is typically paired with route-discovery workflows.

---

## Molecule

Use the same README layout as the working collection roles so Molecule/README validation sees the expected sections and ordering.

```
dependency -> lint -> syntax -> create -> converge -> idempotence -> destroy -> verify
```

---

## License

GPL-3.0-or-later

---

## Author

Chad Elliott

---

## Repository layout (role)

```text
roles/
`-- openshift_tools_ensure_alt_routes_from_list/
    |-- README.md
    |-- defaults/
    |   `-- main.yml
    |-- tasks/
    |   `-- main.yml
    |-- vars/
    |   `-- main.yml
    |-- handlers/
    |   `-- main.yml
    |-- meta/
    |   `-- main.yml
    |-- templates/                # optional
    |-- files/                    # optional
    `-- tests/
        |-- inventory
        `-- test.yml               # optional
```
