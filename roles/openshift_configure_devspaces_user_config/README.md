# Role: openshift_configure_devspaces_user_config

Create Dev Spaces user workspace supporting objects such as secrets, config maps, and a PVC.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- `community.crypto` collection installed for SSH key generation.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Desired state for the user resources. The current tasks create resources when `state: present`. |
| `username` | User name used to build namespace and object names. Required. |
| `certificate_value` | Base64-ready certificate content stored in the user certificate secret. |
| `pvc_size` | Requested PVC size for the workspace volume. |
| `storage_class` | Storage class for the workspace PVC. |
| `ssh_config / known_hosts` | SSH client configuration values stored as mounted secrets. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_devspaces_user_config
      vars:
        state: present
        username: jdoe
        certificate_value: "{{ my_cert_b64 }}"
        pvc_size: 10Gi
        storage_class: gp3-csi
        ssh_config: |
          Host github.com
            User git
        known_hosts: "{{ my_known_hosts }}
```

---

## Behavior Notes

- Creates config and secret objects in the `<username>-devspaces` namespace.
- Generates SSH keys when the expected secrets do not already exist.

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
`-- openshift_configure_devspaces_user_config/
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
