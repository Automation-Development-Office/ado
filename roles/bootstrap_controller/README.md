# Role: bootstrap_controller

Generate and optionally apply **AAP / Controller bootstrap configuration** for the ADO bootstrap framework.

This role is the orchestration layer that ties together the bootstrap collection. It can:

- generate environment variable files
- generate a bootstrap playbook repository
- generate AAP controller configuration artifacts
- load generated job template / workflow YAML
- apply the generated AAP configuration to AAP 2.4 / 2.5+ environments

The role is designed to be used by the bootstrap CLI / UI scaffolding workflow and is the top-level execution role for end-to-end bootstrap generation.


## Notes

This is the first draft README generated from the bootstrap design/work we discussed in chat.
Before committing, I recommend one cleanup pass to align variable tables and examples with the current
`defaults/main.yml` and `tasks/main.yml` in the role directory.

