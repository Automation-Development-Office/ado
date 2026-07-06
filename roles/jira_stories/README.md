# Role: infra.ado.jira_stories

Jira Stories automation role. Primary tasks include: Jira | Normalize legacy and CLI vars; Jira | Validate required vars; Jira | Build list of template files for selected track.

## Role Author

Automation Development Office

## ✅ Role Requirements

- Ansible Core
- Required collections listed in `collections/requirements.yml`
- Inventory or extra variables appropriate for the target platform

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `jira_stories_story_issuetype` | Role input variable used to configure automation behavior. |
| `jira_stories_subtask_issuetype` | Role input variable used to configure automation behavior. |
| `jira_stories_create_subtasks` | Role input variable used to configure automation behavior. |
| `jira_stories_templates_dir` | Role input variable used to configure automation behavior. |
| `jira_stories_feature_key` | Role input variable used to configure automation behavior. |

## 🚀 Role Usage

```yaml
- name: Run jira_stories
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.jira_stories
```

## 🧪 Role Molecule Testing

Run Molecule scenarios from the role directory when a scenario is available.

This role runs tasks such as:

- Jira | Normalize legacy and CLI vars
- Jira | Validate required vars
- Jira | Build list of template files for selected track
- Jira | Process templates for track

```bash
cd roles/jira_stories
molecule test
```

## 📁 Role Structure

```text
roles/jira_stories/
  README.md
  defaults/
  handlers/
  meta/
  tasks/
  tests/
  vars/
```
