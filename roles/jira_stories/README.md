# Role: infra.ado.jira_stories

Generate Jira stories and optional subtasks from track-based templates.

## Role Author

Corey Kyle / Automation Development Office.

## ✅ Role Requirements

- `community.general` collection (uses `community.general.jira`).
- Jira credentials and project details must be provided:
  - `jira_url`
  - `jira_username`
  - `jira_token`
  - `jira_project_key`
- Template files for selected track must be present under this role's
  `templates/` directory structure.

## 📦 Role Variables

Key role variables from `defaults/main.yml` and tasks:

- `jira_stories_track` (default: `platform_4phase`)
- `jira_stories_track_map` (track -> template file/section list)
- `jira_stories_story_issuetype` (default: `Story`)
- `jira_stories_subtask_issuetype` (default: `Sub-task`)
- `jira_stories_create_subtasks` (default: `true`)
- `jira_stories_feature_key` / `jira_stories_feature_field`
- `jira_stories_custom_ac_field`
- `jira_stories_dry_run` (optional, used in task flow)

Compatibility inputs accepted in `tasks/main.yml`:

- `jira_track` -> `jira_stories_track`
- `jira_story_issuetype` -> `jira_stories_story_issuetype`
- `jira_subtask_issuetype` -> `jira_stories_subtask_issuetype`
- `jira_create_subtasks` -> `jira_stories_create_subtasks`
- `jira_custom_ac_field` -> `jira_stories_custom_ac_field`
- `jira_feature_key` -> `jira_stories_feature_key`
- `jira_feature_field` -> `jira_stories_feature_field`

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.jira_stories
      vars:
        jira_url: "https://jira.example.com"
        jira_username: "automation-user"
        jira_token: "{{ vault_jira_token }}"
        jira_project_key: "PROJ"
        jira_stories_track: "platform_4phase"
        jira_stories_create_subtasks: true
        product: "my-product"
        group: "platform"
```

## 🧪 Role Molecule Testing

No extension-level Molecule scenario is currently defined for this role in
`extensions/molecule/integration_*`.

Use the README verification script to validate format:

```bash
python scripts/verify_readme.py roles/jira_stories/README.md --template docs/templates/role_readme_format_template.md
```

## 📁 Role Structure

```text
jira_stories/
├── defaults/
│   └── main.yml
├── meta/
│   └── main.yml
├── tasks/
│   ├── main.yml
│   └── process_one_template.yml
├── templates/
│   ├── day2/
│   ├── phases/
│   ├── special/
│   └── tracks/
└── README.md
```
