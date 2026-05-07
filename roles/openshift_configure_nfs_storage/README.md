# Role: openshift_configure_nfs_storage

Configure NFS-backed storage resources for OpenShift.

---

## Requirements

- OpenShift/Kubernetes API access.
- Any manifest files or external resources referenced by the role must exist before execution.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Desired state for the NFS storage workflow. |
| `name_space` | Namespace used by the storage resources when applicable. |
| `storage_class_name` | Storage class name when creating NFS-backed storage objects. |
| `nfs_server / nfs_path` | Typical caller-provided NFS endpoint values for the backing export. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_nfs_storage
      vars:
        state: present
        name_space: openshift-storage
        storage_class_name: nfs-storage
        nfs_server: nfs.example.com
        nfs_path: /exports/ocp
```

---

## Behavior Notes

- Use this README format as the role contract even if the implementation is still evolving.
- Keep the example variables aligned with the live task files as the role grows.

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
`-- openshift_configure_nfs_storage/
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
