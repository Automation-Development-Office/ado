# Role: infra.ado.utilities_utilities_rhel_facts

Collect a concise set of **RHEL host facts** using _raw, POSIX-friendly commands_ (works on RHEL **7/8/9/10** without requiring Python on the target), normalize them into stable variables, and emit a **human‑readable summary**.

- Uses only `ansible.builtin.raw` + core tools (`systemctl`, `free`, `ip`, `awk`, etc.).
- Exposes normalized variables under the `rhel_facts_*` namespace.
- Provides `rhel_facts_fact_lines` (a ready‑to‑print list of one‑line summaries).

---

## Requirements

- Target hosts reachable by Ansible (typically `become: true`).
- POSIX shell and common utilities available on the managed host:
  `systemctl`, `ip`, `awk`, `free`, `date`, `hostname`, `dnf`/`yum`.
- No Python required on the managed host (controller still needs Ansible).

---

## Variables

This role has **no required input variables**. It gathers and normalizes facts automatically.

### Exported variables

| Variable | Type | Description |
|---------|------|-------------|
| `rhel_facts_tuned_active` | bool | Whether `tuned` is active. |
| `rhel_facts_fw_active` | bool | Whether `firewalld` is active. |
| `rhel_facts_used_mb`, `rhel_facts_total_mb` | int | Memory in MB (used/total). |
| `rhel_facts_used_g`, `rhel_facts_total_g` | float | Memory in GiB (used/total). |
| `rhel_facts_rel_line` | string | Raw `/etc/redhat-release` line. |
| `rhel_facts_rel_sane` | string | Normalized release string (e.g., `RedHat 9.4`). |
| `rhel_facts_time_iso` | string | UTC time in ISO‑8601. |
| `rhel_facts_hostname` | string | FQDN (fallback to short hostname). |
| `rhel_facts_ip_cidr` | string | Primary IPv4 in CIDR (e.g., `10.0.0.10/24`). |
| `rhel_facts_ip_only` | string | IPv4 address only. |
| `rhel_facts_prefix` | string | CIDR prefix length (e.g., `24` or empty). |
| `rhel_facts_gw_line` | string | Default route line from `ip route`. |
| `rhel_facts_dns_list` | list[str] | DNS nameservers from `/etc/resolv.conf`. |
| `rhel_facts_rhsm_host` | string | Hostname from `/etc/rhsm/rhsm.conf` (if any). |
| `rhel_facts_repo_lines` | list[str] | Enabled repo lines (`<id>\t<name>`). |
| `rhel_facts_repo_count` | int | Count of enabled repos. |
| `rhel_facts_is_satellite` | bool | True if RHSM hostname doesn’t contain `redhat.com`. |
| `rhel_facts_repo_summary` | string | e.g., `5 repos; satellite` or `0 repos; rhsm`. |
| `rhel_facts_fact_lines` | list[str] | Prebuilt one‑line summaries ready to print. |

> Note: When information is unavailable on a host, related variables are set to safe defaults (`''`, `0`, `[]`, or `false`).

---

## Examples

### Collect and print the human summary

```yaml
- hosts: all
  gather_facts: false
  become: true
  roles:
    - role: infra.ado.utilities_utilities_rhel_facts

  tasks:
    - name: Show pretty summary
      ansible.builtin.debug:
        msg: "{{ rhel_facts_fact_lines | join('\n') }}"
```

### Use a specific value in another task

```yaml
- name: Fail if SELinux is disabled
  ansible.builtin.fail:
    msg: "SELinux must be enabled"
  when: rhel_facts_sel_text == 'disabled'
```

---

## Behavior Notes

- Designed for **RHEL 7/8/9/10**; avoids fragile `gather_subset` and works even if Python isn’t installed on the target.
- Repository info is extracted with `dnf -q repolist -v` or `yum -q repolist -v` (whichever exists).
- Networking is derived from `ip route` and `ip -o -4 addr` with safe fallbacks.
- All outputs are computed in **separate tasks** to avoid Ansible forward‑reference pitfalls.

---

## 🧪 Molecule

This role no longer includes a dedicated Molecule scenario or platform-specific Molecule playbooks.

> Molecule tests for `platform_satellite_install` have been removed from the repository.

## Author

- Chad Elliott (<chelliot@redhat.com>)

---

## Repository layout (role)

```text
.
├── defaults
│   └── main.yml
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── README.md                # ← this file
├── tasks
│   └── main.yml
├── tests
│   ├── inventory
│   └── test.yml
└── vars
    └── main.yml
```
