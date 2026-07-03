# Role: bootstrap_generate_playbook_repo

Generate a **bootstrap playbook repository** from the selected bootstrap components and applications.

This role seeds a destination repository with:

- inventory
- `group_vars`
- playbooks
- controller config scaffolding
- README / support files
- optional Git initialization / commit / push behavior


## Notes

This is the first draft README generated from the bootstrap design/work we discussed in chat.
Before committing, I recommend one cleanup pass to align variable tables and examples with the current
`defaults/main.yml` and `tasks/main.yml` in the role directory.

