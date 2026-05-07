# Role: openshift_configure_compliance_remidiation_acs

Trigger an ACS remediation request by calling the ACS API when remediation is enabled.

---

## Requirements

- Network access from the automation controller to the ACS API endpoint.
- A valid ACS bearer token.

---

## Variables

| Variable | Description |
|---------|-------------|
| `remediation` | Boolean toggle. When `true`, the API call is made. |
| `acs_api_url` | ACS API host name or endpoint used to build the remediation URL. Required when remediation is enabled. |
| `acs_token` | Bearer token used for ACS authentication. Required when remediation is enabled. |
| `compliance_profile` | Compliance profile value sent in the request body. |
| `scan_id` | Scan identifier sent in the request body. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_configure_compliance_remidiation_acs
      vars:
        remediation: true
        acs_api_url: acs.example.com
        acs_token: "{{ vault_acs_token }}"
        compliance_profile: ocp4-cis
        scan_id: latest-scan
```

---

## Behavior Notes

- Uses `ansible.builtin.uri` to post to the ACS remediation endpoint.
- When `remediation` is false, the role performs no API change.

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
`-- openshift_configure_compliance_remidiation_acs/
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
