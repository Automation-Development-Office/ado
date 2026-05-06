# Role: `cron`

This Ansible role manages cron jobs, including special time-based entries (e.g., `@reboot`, `@hourly`, `@daily`) for Linux systems.
It supports flexible addition, removal, and verification of cron jobs using Ansible variables.

> **⚠️ Note:**
> This role is intended for Linux systems with cron installed. Ensure your target hosts support cron management.

## ✅ Role Requirements

- Ansible >= 2.9
- The target host must support cron and be reachable by Ansible.
- No additional collections required.

## 📦 Role Variables

| Variable            | Description                                             | Required | Default  |
|---------------------|---------------------------------------------------------|----------|----------|
| `cron_type`         | Type of cron jobs to manage (`special`, etc.)           | ❌       | `special`|
| `cron_state`        | State of cron jobs (`present`, `absent`)                | ❌       | `present`|
| `cron_yearly_jobs`  | List of yearly cron jobs (`[{ name, job }]`)            | ❌       | `[]`     |
| `cron_monthly_jobs` | List of monthly cron jobs (`[{ name, job }]`)           | ❌       | `[]`     |
| `cron_weekly_jobs`  | List of weekly cron jobs (`[{ name, job }]`)            | ❌       | `[]`     |
| `cron_daily_jobs`   | List of daily cron jobs (`[{ name, job }]`)             | ❌       | `[]`     |
| `cron_hourly_jobs`  | List of hourly cron jobs (`[{ name, job }]`)            | ❌       | `[]`     |
| `cron_reboot_jobs`  | List of reboot cron jobs (`[{ name, job }]`)            | ❌       | `[]`     |
| `cron_annual_jobs`  | List of annual cron jobs (`[{ name, job }]`)            | ❌       | `[]`     |

See `defaults/main.yml` and `vars/main.yml` for all available variables.

## 🚀 Usage

Define the desired cron jobs in your playbook or inventory using the variables above.

## 🔧 Tasks Overview

- **Special Cron Jobs** (`special_crons.yml`):
  - Manages jobs for special time entries (`@reboot`, `@hourly`, etc.) using Ansible's cron module.
- **Main Task File** (`main.yml`):
  - Imports and runs the appropriate cron management tasks.

## 📁 Structure

```
cron/
├── defaults/
│   └── main.yml
├── vars/
│   └── main.yml
├── tasks/
│   ├── main.yml
│   └── special_crons.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── molecule/
│   ├── full_special/
│   ├── full_special_removal/
│   ├── single_special/
│   ├── single_special_removal/
│   ├── verify_docs/
│   └── ...
├── files/
├── templates/
├── tests/
│   ├── full_special.yml
│   ├── full_special_removal.yml
│   ├── single_special_removal.yml
│   ├── single_special.yml
│   ├── test.yml
│   ├── verify_docs.yml
│   ├── verify_full_special.yml
│   ├── verify_full_special_removal.yml
│   ├── verify_single_special.yml
│   ├── verify_single_special_removal.yml
│   └── ...
└── README.md
```

## License

BSD

## Author Information

Automation Development Office
