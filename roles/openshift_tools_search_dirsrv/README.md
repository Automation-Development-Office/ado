# Role: openshift_tools_search_dirsrv

Run LDAP search queries inside a running directory server pod and print or capture the results.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- A running directory server pod that matches the configured label selector.

---

## Variables

| Variable | Description |
|---------|-------------|
| `dirsrv_search_target_namespace` | Namespace to search for the directory server pod. Defaults to `dirsrv`. |
| `dirsrv_search_app_label` | Pod label selector used to find the target pod. |
| `dirsrv_search_container_name` | Container name used by the exec task. |
| `dirsrv_search_bind_dn / dirsrv_search_suffix` | LDAP bind DN and directory suffix used by the generated search script. |
| `dirsrv_search_queries` | List of query definitions to run inside the container. |
| `dirsrv_search_print_only` | When true, prints the search output through `debug`. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_tools_search_dirsrv
      vars:
        dirsrv_search_target_namespace: dirsrv
        dirsrv_search_app_label: app=dirsrv
        dirsrv_search_suffix: dc=example,dc=com
```

---

## Behavior Notes

- Locates a directory server pod, renders `templates/run_search.sh.j2`, and executes it inside the container.
- Built-in default queries cover common user and group lookups.

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
`-- openshift_tools_search_dirsrv/
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
