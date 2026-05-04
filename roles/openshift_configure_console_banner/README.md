# Role: openshift_configure_console_banner

Manage OpenShift console notification banners using `ConsoleNotification` resources.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.

---

## Variables

| Variable | Description |
|---------|-------------|
| `state` | Desired state: `present`, `new`, or `absent`. Defaults to `present`. |
| `console_banner_text` | Banner text. Required for `present` and `new`. |
| `console_banner_name` | Fixed banner name used by the `new` workflow. Defaults to `ado-banner`. |
| `console_banner_name_prefix` | Prefix used to identify ADO-managed banner resources. Defaults to `ado-banner`. |
| `console_banner_location` | Banner location in the console UI. Defaults to `BannerTop`. |
| `console_banner_background_color` | Background color for the banner. |
| `console_banner_text_color` | Foreground text color for the banner. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_console_banner
      vars:
        state: present
        console_banner_text: Hello! RHLAB OpenShift | Production
        console_banner_location: BannerTop
        console_banner_background_color: '#1f7a1f'
        console_banner_text_color: '#ffffff'
```

---

## Behavior Notes

- The `present` path creates a deterministic per-message banner if one does not already exist.
- The `new` path deletes existing ADO-managed banners before creating a single replacement banner.
- The `absent` path only removes ADO-managed banners matched by label or prefix.

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
`-- openshift_configure_console_banner/
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
