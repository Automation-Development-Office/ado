# Role: bootstrap_flatten_vars

Flatten a nested bootstrap component configuration structure into a simpler variable map that downstream bootstrap roles can consume consistently.

This role is a **data-shaping / normalization role** used by the bootstrap framework. It is not responsible for generating files or applying AAP resources directly. Instead, it takes structured component input and produces a normalized variable set for later roles such as:

- `bootstrap_generate_env_vars`
- `bootstrap_generate_playbook_repo`
- `bootstrap_controller`


## Notes

This is the first draft README generated from the bootstrap design/work we discussed in chat.
Before committing, I recommend one cleanup pass to align variable tables and examples with the current
`defaults/main.yml` and `tasks/main.yml` in the role directory.

