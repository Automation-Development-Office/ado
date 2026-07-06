# Role: bootstrap_resolve_component

Resolve a selected bootstrap component into the **effective merged component configuration** used by the bootstrap framework.

This role is the framework's **component registry resolver**. It takes a requested component (for example `openshift`, `rhel`, `patching`, or an application component) and merges:

- framework defaults
- component registry defaults
- environment-specific overrides
- aliases / normalized names where needed


## Notes

This is the first draft README generated from the bootstrap design/work we discussed in chat.
Before committing, I recommend one cleanup pass to align variable tables and examples with the current
`defaults/main.yml` and `tasks/main.yml` in the role directory.

