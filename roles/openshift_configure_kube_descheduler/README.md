# Role: openshift_configure_kube_descheduler

Create or update a `KubeDescheduler` custom resource from a Jinja template.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- Kube Descheduler operator installed before this role runs.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Outer role guard used by `tasks/main.yml`. Use `present` for the current workflow. |
| `kube_descheduler_state` | State passed to the `kubernetes.core.k8s` task for the CR. |
| `instance_name` | Instance name rendered into the template. |
| `scheduling_interval` | Scheduling interval rendered into the template. |
| `descheduler_profiles` | List of descheduler profiles rendered into the template. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_kube_descheduler
      vars:
        state: present
        kube_descheduler_state: present
        instance_name: cluster
        scheduling_interval: 300
        descheduler_profiles:
          - AffinityAndTaints
          - TopologyAndDuplicates
```

---

## Behavior Notes

- Renders `templates/kube_cluster.j2` and applies it through `kubernetes.core.k8s`.
- This role assumes the operator and required CRDs are already available.

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
`-- openshift_configure_kube_descheduler/
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
