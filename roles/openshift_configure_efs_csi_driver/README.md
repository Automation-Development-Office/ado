# Role: openshift_configure_efs_csi_driver

Create an AWS EFS CSI storage class backed by the EFS CSI provisioner.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- The AWS EFS CSI driver must already be installed in the cluster.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Desired state. The current task creates the storage class when `state: present`. |
| `storage_class_name` | Name of the EFS-backed storage class. Required. |
| `efs_filesystem_id` | EFS filesystem identifier used by the storage class. Required. |
| `base_path / base_path_perms` | Base directory and permissions used by the access point provisioner. |
| `gid_start / gid_end` | GID range reserved for access point provisioning. |
| `reclaim_policy / binding_mode` | Storage class reclaim policy and binding mode values. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_efs_csi_driver
      vars:
        state: present
        storage_class_name: efs-sc
        efs_filesystem_id: fs-12345678
        base_path: /team-a
        base_path_perms: '700'
        gid_start: '1000'
        gid_end: '2000'
        reclaim_policy: Delete
        binding_mode: Immediate
```

---

## Behavior Notes

- Creates a `StorageClass` using the `efs.csi.aws.com` provisioner.
- The role does not install the operator; it only manages the storage class resource.

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
`-- openshift_configure_efs_csi_driver/
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
