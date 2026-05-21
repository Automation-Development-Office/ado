# Role: utilities_jira

This role provides a repeatable framework for generating Jira stories and subtasks
from structured templates and selected delivery tracks.

Supported work styles include:

- Platform/service delivery (phase-based)
- Ansible collection/code delivery
- Day-2 operations
- Engineering work types (`spike`, `bugfix`, `feature`)

---

## Core Concepts

### Phases vs Tracks

| Dimension | Meaning |
| --- | --- |
| **Phase** | Position in the delivery lifecycle (design -> deploy -> validate -> operate) |
| **Track** | Work type (`platform_4phase`, `collections_2phase`, `day2`, `spike`, etc.) |

---

## Default Delivery Model

The default platform flow uses 4 phases:

1. Phase 1: Kickoff, readiness, and design
2. Phase 2: Deployment and core configuration
3. Phase 3: Validation, adoption, and enablement
4. Phase 4: Operations, governance, and handoff

---

## Track Selection Matrix

| Track | Purpose | Typical Use | Template Files | Section Values |
| --- | --- | --- | --- | --- |
| `platform_4phase` | Full platform/service delivery | Most products/services | `templates/phases/story_phase1.yml` to `story_phase4.yml` | `phase1..phase4` |
| `collections_2phase` | Deliver Ansible collection code | Collection work | `templates/tracks/collections_phase1.yml`, `collections_phase2.yml` | `phase1,phase2` |
| `mfa_2phase` | MFA enablement + handoff | MFA deployments | `templates/tracks/mfa_phase1.yml`, `mfa_phase2.yml` | `phase1,phase2` |
| `day2` | Operational issue handling | Break/fix incidents | `templates/day2/adhoc_day2.yml` | `operations` |
| `spike` | Timeboxed discovery | Unknowns/evaluation | `templates/special/adhoc_spike.yml` | `discovery` |
| `bugfix` | Fix broken behavior | Automation defects | `templates/special/adhoc_bugfix.yml` | `delivery` |
| `feature` | Add capability | Role enhancements | `templates/special/adhoc_feature.yml` | `delivery` |

---

## Running the Role

### 1) Configure Jira credentials

Set these through environment variables, vault, or vars files.

Required canonical variables:

- `utilities_jira_url`
- `utilities_jira_username`
- `utilities_jira_token`
- `utilities_jira_project_key`

Supported compatibility aliases:

- `jira_url`
- `jira_username`
- `jira_token`
- `jira_project_key`

### 2) Choose a track

Set `utilities_jira_track` to one of:
`platform_4phase`, `collections_2phase`, `mfa_2phase`, `day2`, `spike`, `bugfix`, `feature`.

Compatibility alias: `jira_track`.

### 3) Provide template inputs

Common template fields:

- `product`
- `group`
- `enviroment`
- `role_name`
- `section`

Track-specific templates may add additional fields.

---

## Optional Feature/Epic Link

Optional canonical variables:

- `utilities_jira_feature_key` (for example `TET-123`)
- `utilities_jira_feature_field` (for example `customfield_XXXXX`)

Supported compatibility aliases:

- `jira_feature_key`
- `jira_feature_field`

When both are set, created stories include:
`fields[utilities_jira_feature_field] = utilities_jira_feature_key`.

---

## Notes

- Default to phase-based tracks for platform/service work
- Use `spike`, `bugfix`, `feature`, `day2`, and `collections_*` when appropriate
- Keep templates consistent and automation-friendly
