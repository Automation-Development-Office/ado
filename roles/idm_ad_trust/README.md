# Role: infra.ado.idm_ad_trust

Establish a **two-way** IdM ↔ Active Directory trust and map AD-only users into
IdM POSIX groups / sudo so they can SSH and sudo on IdM-enrolled Linux clients
without existing in IdM.

Derived from:

- `SCRUBBED-AvMC-IPA-Installation-Configuration-v1.0.pdf` §2.6 / §2.8
- MFA lab notes (DNS forward zone, `ldap_idmap_range_size`, external groups)

## Lab defaults (2026-08-11)

| Component | Value |
|-----------|-------|
| IdM | `idm-trust.dev.rhlab` → `192.168.0.63` (realm `DEV.RHLAB`) |
| AD DC | `adwindows.ad.lab` → `192.168.0.61` (OCP virt NS `window-vms`) |
| AD realm | `AD.LAB` |

## Required secrets

- `idm_ad_trust_ipa_admin_password` / `vault_idm_admin_password`
- `idm_ad_trust_ad_admin_password` / `vault_ad_trust_admin_password`

## Pre-flight on AD

Create a **conditional forwarder** on the AD DNS server for the IdM domain
(for example `dev.rhlab` → `192.168.0.63`) so AD can resolve IdM SRV records.
Without that, two-way trust fails with
`AD DC was unable to reach any IPA domain controller`.

One-way trust (`idm_ad_trust_two_way: false`) still allows AD users to authenticate
to IdM/Linux and does not require AD to reach IdM DCs.

## Usage

```yaml
- hosts: all
  become: true
  vars:
    idm_ad_trust_ipa_admin_password: "{{ vault_idm_admin_password }}"
    idm_ad_trust_ad_admin_password: "{{ vault_ad_trust_admin_password }}"
    idm_ad_trust_map_ad_admins_group: "Domain Admins@AD.LAB"
    idm_ad_trust_sudo_ad_users:
      - "Administrator@AD.LAB"
  roles:
    - role: infra.ado.idm_ad_trust
```

Bootstrap playbook: `playbooks/idm/ado-manage-ad-trust-bootstrap.yml`
Job template: `ADO | IdM Manage AD Trust` (app option `idm_ad_trust_install`)

## Client checklist (after trust)

On each IdM client that should accept AD users:

1. DNS must resolve `AD.LAB` (IdM forward zone or `/etc/resolv.conf` path).
2. SSSD domains include IdM (trust provides AD via IdM).
3. Useful AD subdomain knobs (from MFA lab):

```ini
[domain/ad.lab]
krb5_auth_timeout = 120
ad_enable_gc = False
krb5_validate = False
```

Also ensure `krb5_validate = False` under the **IdM** domain stanza if SSH
account checks fail after password auth succeeds (`id`/`kinit` OK, `ssh` denied).

4. HBAC: default `allow_all` is enough for login; sudo requires the external →
   POSIX → sudorule mapping this role creates.

## Smart card / PKINIT

Out of scope for this role. See the smartcard IdM+AD guide. Password SSH/sudo
for AD-only users is the first milestone.
