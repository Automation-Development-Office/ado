# Role: openshift_tools_ensure_component_route

Ensure a component route and optional alternate route match the requested service, host, and TLS settings.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.

---

## Variables

| Variable | Description |
|---------|-------------|
| `ensure_component_route_namespace` | Namespace that owns the route resources. |
| `ensure_component_route_route_name` | Primary route name. |
| `ensure_component_route_route_host` | Primary route host name. |
| `ensure_component_route_route_name_alt / ensure_component_route_route_host_alt` | Optional alternate route name and host values. |
| `backend_svc / backend_port` | Service name and target port for the route backend. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_tools_ensure_component_route
      vars:
        ensure_component_route_namespace: grafana
        ensure_component_route_route_name: grafana
        ensure_component_route_route_host: grafana.apps.example.com
        ensure_component_route_route_name_alt: grafana-alt
        ensure_component_route_route_host_alt: grafana-alt.apps.example.com
        backend_svc: grafana-service
        backend_port: https
```

---

## Behavior Notes

- Compares the live route spec to the requested values and replaces incorrect routes when necessary.
- Can manage both a primary route and an alternate route in a single run.

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
`-- openshift_tools_ensure_component_route/
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
