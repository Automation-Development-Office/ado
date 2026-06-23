# Role: `ocp_console_banner`

Manage OpenShift console notification banners using `ConsoleNotification` resources.

## Role Author

Chad Elliott

## ✅ Role Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.

## 📦 Role Variables

| Variable | Description | Required | Default |
| -------- | ----------- | -------- | ------- |
| `state` | Desired state: `present`, `new`, or `absent`. | No | `present` |
| `ocp_console_banner_text` | Banner text content. | Yes* | N/A |
| `ocp_console_banner_name` | Fixed banner name used by the `new` workflow. | No | `ado-banner` |
| `ocp_console_banner_name_prefix` | Prefix used to identify ADO-managed banners. | No | `ado-banner` |
| `ocp_console_banner_location` | Banner location in the console UI. | No | `BannerTop` |
| `ocp_console_banner_background_color` | Banner background color. | No | `#1f7a1f` |
| `ocp_console_banner_text_color` | Banner text color. | No | `#ffffff` |

> **Notes:**
> \* Required when `state` is `present` or `new`.

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_console_banner
      vars:
        state: present
        ocp_console_banner_text: Hello! RHLAB OpenShift | Production
        ocp_console_banner_location: BannerTop
        ocp_console_banner_background_color: "#1f7a1f"
        ocp_console_banner_text_color: "#ffffff"
```

## Behavior Notes

- The `present` path creates a deterministic per-message banner if one does not already exist.
- The `new` path deletes existing ADO-managed banners before creating a single replacement banner.
- The `absent` path only removes ADO-managed banners matched by label or prefix.

## 🧪 Role Molecule Testing

This role has two Molecule paths:

- Role-local scenario at `roles/ocp_console_banner/molecule/default`.
- Extension-level scenario at `extensions/molecule/integration_ocp_console_banner`
  using shared playbooks in `extensions/molecule/utils/playbooks`.

Run the extension scenario from `extensions/molecule`:

```bash
molecule test -s integration_ocp_console_banner
```

## 📁 Role Structure

```text
ocp_console_banner/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── molecule/
│   └── default/
│       ├── converge.yml
│       ├── destroy.yml
│       ├── molecule.yml
│       ├── README.md
│       ├── TEST.md
│       └── verify.yml
├── README.md
├── tasks/
│   └── main.yml
├── tests/
│   └── inventory
└── vars/
    └── main.yml
```

## License

GPL-3.0-or-later
