# Role: infra.ado.bootstrap_generate_playbook_repo

Create or refresh the generated bootstrap playbook repository structure used by
ADO component automation.

## Role Author

Automation Development Office

## Platform coverage

Playbooks in `bootstrap_generate_playbook_repo_generated_playbooks` set
`target_platform` to `openshift` or `linux`. See the collection
[Bootstrap coverage](../../README.md#bootstrap-coverage-openshift-vs-rhel)
tables for a simple OpenShift vs RHEL install/configure checklist.

## ✅ Role Requirements

- Ansible Core
- Write access to the target bootstrap repository directory
- Optional Git remote credentials when automatic commit and push is enabled
- Seed playbook content bundled with this collection

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `bootstrap_generate_playbook_repo_dest` | Destination repository root for generated files. |
| `bootstrap_generate_playbook_repo_seed_src` | Source directory for baseline repository seed files. |
| `bootstrap_generate_playbook_repo_force` | Overwrites generated content when true. |
| `bootstrap_generate_playbook_repo_git_mode` | Git behavior, such as manual or automatic push flow. |
| `bootstrap_generate_playbook_repo_git_remote` | Git remote name to configure or update. |
| `bootstrap_generate_playbook_repo_git_branch` | Branch used for generated repository commits. |
| `bootstrap_generate_playbook_repo_git_message` | Commit message for generated content. |
| `bootstrap_generate_playbook_repo_git_token` | Optional token used for non-interactive Git pushes. |
| `bootstrap_generate_playbook_repo_git_sync_before_push` | Rebase on the remote branch before pushing generated commits. Defaults to `true`. |
| `bootstrap_generate_playbook_repo_write_galaxy_requirements` | When true, write `collections/requirements.yml` so Contoller installs collections from Hub/Galaxy. Default `false` (no Hub). |
| `bootstrap_generate_playbook_repo_infra_ado_collection_version` | Optional pin used only when Galaxy requirements are written. Empty means latest. |
| `bootstrap_generate_playbook_repo_component` | Component group to generate, such as `all`, `openshift`, or `rhel`. |
| `bootstrap_generate_playbook_repo_component_map` | Maps component selections to generated playbook groups. |
| `bootstrap_generate_playbook_repo_generated_playbooks` | Manifest of bundled playbooks copied into the generated repository. |

When Hub collection update is off (default), this role vendors `infra.ado`
into `collections/ansible_collections/infra/ado` and does **not** write
Galaxy `collections/requirements.yml`, so Contoller project sync does not
talk to Hub. When Hub update is on, vendored `infra.ado` is removed and
requirements.yml is written for Galaxy/Hub install.

## 🚀 Role Usage

```yaml
- name: Generate bootstrap playbook repository
  hosts: localhost
  gather_facts: false
  vars:
    bootstrap_generate_playbook_repo_dest: "{{ playbook_dir }}"
    bootstrap_generate_playbook_repo_component: all
  roles:
    - role: infra.ado.bootstrap_generate_playbook_repo
```

## 🧪 Role Molecule Testing

Run focused linting against the role and validate generated content with the
bootstrap sample CLI repository.

```bash
ansible-lint --offline roles/bootstrap_generate_playbook_repo
yamllint roles/bootstrap_generate_playbook_repo/tasks
```

## 📁 Role Structure

```text
roles/bootstrap_generate_playbook_repo/
  defaults/main.yml
  files/playbook_repo_seed/
  files/playbooks/
  tasks/main.yml
  README.md
```
