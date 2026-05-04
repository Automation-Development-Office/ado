# Role: openshift_tools_discover_routes

Discover OpenShift routes and expose the resulting route data for downstream automation.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.

---

## Variables

| Variable | Description |
|---------|-------------|
| `name_space` | Namespace to inspect for route resources. |
| `discover_routes_label_selectors` | Optional label selectors used to filter routes. |
| `discover_routes_name_filter` | Optional route name filter used by the role. |
| `discover_routes_output_var` | Optional variable name used to store discovered route data. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_tools_discover_routes
      vars:
        name_space: grafana
        discover_routes_label_selectors:
          - app.kubernetes.io/name=grafana
```

---

## Behavior Notes

- Use this role to build a route inventory for later tasks such as alternate-route management.
- Keep the README aligned with any future filters added to the route discovery workflow.

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
`-- openshift_tools_discover_routes/
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
