# Role: bootstrap_generate_env_vars

Generate bootstrap **environment variable files** for the selected environment and component set.

This role renders the `group_vars/all/<env>/` structure used by the generated bootstrap playbook repository and CLI/UI workflows.

Typical outputs include:

- application / platform vars files
- component vars files
- component vault files


## Notes

This is the first draft README generated from the bootstrap design/work we discussed in chat.
Before committing, I recommend one cleanup pass to align variable tables and examples with the current
`defaults/main.yml` and `tasks/main.yml` in the role directory.

