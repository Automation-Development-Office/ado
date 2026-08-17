# Role: infra.ado.acs_report

Generate Red Hat Advanced Cluster Security (RHACS) vulnerability reports from
Central's workload export API. Ports the `rhacs-report.sh` workflow into an
Ansible role for ADO bootstrap / Controller job templates.

## Role Author

Automation Development Office

## Modes

| `acs_report_mode` | Script flag | Output |
|-------------------|-------------|--------|
| `raw` | `--raw` | Live workloads, Critical+Important, all sources, component table |
| `rhsource` | `--rhsource` | Same, Red Hat CVE/errata source only |
| `age` | `--age` | Red Hat source, age buckets `>15` / `>30` / `>90` days |
| `all` | `--all` (alone) | Scrubbed CSV of all severities/sources (live + inactive) |

Scope modifiers:

| Variable | Script flag | Effect |
|----------|-------------|--------|
| `acs_report_all_scope: true` | `--all` with raw/rhsource | Expand to all product groups |
| `acs_report_rhsre: true` | `--rhsre` | ROSA/SRE responsibility boundary only |
| `acs_report_component` | `--component` | Limit to one group (`acm`, `devspaces`, …) |
| `acs_report_show_sev: true` | `--sev` | Add Critical/High columns |

## Role Variables

| Variable | Description |
|----------|-------------|
| `acs_report_mode` | `raw` \| `rhsource` \| `age` \| `all`. Default `rhsource`. |
| `acs_report_outdir` | Output directory for CSV / summary JSON / text. |
| `acs_central_url` | Central base URL. Derived from route + `app_domain` when empty. |
| `acs_api_token` | Bearer token (preferred). Also accepts `ROX_API_TOKEN` env. |
| `acs_admin_user` / `acs_admin_password` | Basic auth fallback when token unset. |
| `acs_namespace` | Namespace for route derivation. Default `stackrox`. |

## Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.acs_report
      vars:
        acs_report_mode: rhsource
        acs_report_show_sev: true
        acs_central_url: https://central-stackrox.apps.example.com
        acs_api_token: "{{ vault_acs_api_token }}"
        acs_report_outdir: /tmp/acs-reports
```

Local CLI (same files the role stages; invoke with bash because the
collection copy has no shebang — ansible-test forbids `#!/bin/bash` on
non-module files. The role adds the shebang after copy to `/tmp`):

```bash
export ROX_ENDPOINT=https://central-stackrox.apps.example.com
export ROX_API_TOKEN=...
bash roles/acs_report/files/rhacs-report.sh --rhsource --sev
```

## Grafana sample dashboard

`files/grafana/rhacs-vulnerability-overview.json` — **RHACS Vulnerability Posture**
dashboard (UID `ado-rhacs-vuln-posture`):

- Totals: unique CVEs, Critical, Important
- Bar charts: findings by component for `--rhsource` and `--raw`
- Stacked Critical vs Important concentration charts
- Daily discovery inflow + cumulative backlog growth

`files/grafana/sample-prod-summary.json` — numeric views used to build that dashboard.

The same dashboard is also seeded for playbook-repo copy-out next to the
Openshift Grafana templates:

`roles/bootstrap_generate_playbook_repo/files/playbook_repo_seed/templates/RHACS/dashboards/rhacs-vulnerability-overview.json`

Default `grafana_folders` includes a **RHACS** folder pointing at
`templates/RHACS` (with Openshift under `templates/Openshift`).

## Artifacts

- Slack-friendly text table (stdout + `RHACS_report_<mode>_<stamp>.txt`)
- `RHACS_summary_<mode>_<stamp>.json` for raw/rhsource/age
- `RHACS_Vulnerability_Report_SCRUBBED_<stamp>.csv` for mode `all`

## Structure

```text
roles/acs_report/
  defaults/main.yml
  meta/main.yml
  tasks/main.yml
  README.md
  files/
    rhacs-report.sh
    rhacs_report_parser.py
    grafana/
      rhacs-vulnerability-overview.json
      sample-prod-summary.json
```
