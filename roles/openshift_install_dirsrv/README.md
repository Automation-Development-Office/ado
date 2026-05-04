# Role: openshift_install_dirsrv

Deploy a 389 Directory Server stack including service account, services, StatefulSet, and optional certificate/bootstrap flows.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- Vault values for the `dirsrv` component must be available when bootstrap or replication is enabled.

---

## Variables

| Variable | Description |
|---------|-------------|
| `name_space` | Target namespace for the directory server deployment. |
| `statefulset_name` | StatefulSet name for the deployment. Required. |
| `storage_class_name` | Storage class used by the PVC template. Required. |
| `sa_name / scc_name` | Service account and SCC binding inputs. |
| `dm_secret_name / dm_secret_key` | Secret name and key used for the Directory Manager password. |
| `enable_certificate / enable_bootstrap / enable_replication` | Feature toggles for optional certificate, bootstrap, and replication workflows. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_install_dirsrv
      vars:
        name_space: dirsrv
        statefulset_name: dirsrv
        storage_class_name: gp3-csi
        sa_name: dirsrv
        scc_name: anyuid
        dm_secret_name: dirsrv-admin
        dm_secret_key: password
```

---

## Behavior Notes

- Builds several derived facts from component defaults and vault-provided `dirsrv` values.
- Creates supporting service, secret, and StatefulSet resources as part of one role execution.

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
`-- openshift_install_dirsrv/
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
