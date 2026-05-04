# Role: openshift_configure_iscsi_storage

Configure Synology-backed iSCSI storage resources when no default storage class is already present.

---

## Requirements

- Cluster access through `community.kubernetes` modules.
- The files referenced by `synology_dir` and `deploy_dir` must exist on the control node.

---

## Variables

| Variable | Description |
|---------|-------------|
| `kubeconfig_tmp` | Kubeconfig path used by the role. Required. |
| `synology_dir` | Directory containing Synology storage manifests and `client-info.yml`. Required. |
| `deploy_dir` | Directory containing CSI deployment manifests. Required. |
| `state` | This role currently implements the create path for storage resources. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_iscsi_storage
      vars:
        kubeconfig_tmp: /tmp/kubeconfig
        synology_dir: /opt/synology
        deploy_dir: /opt/synology/deploy
        state: present
```

---

## Behavior Notes

- Checks for an existing default storage class before applying Synology manifests.
- Applies namespace, secret, driver, and snapshot manifests when provisioning is needed.

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
`-- openshift_configure_iscsi_storage/
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
