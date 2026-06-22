## Summary

<!-- Briefly describe what changed and why (1–3 sentences). -->

## Related issues

<!-- Link related work. Examples: Fixes #123, Relates to #456 -->

-

## Type of change

<!-- Mark all that apply. -->

- [ ] New or updated collection role
- [ ] New or updated Molecule scenario (`extensions/molecule/`)
- [ ] CI / GitHub Actions workflow
- [ ] Scripts or developer tooling
- [ ] Documentation only
- [ ] Bug fix
- [ ] Other (describe below)

## Collection impact

<!-- List the main paths touched so reviewers know where to focus. -->

| Area | Path(s) |
| --- | --- |
| Role(s) | <!-- e.g. roles/satellite_content_view --> |
| Molecule scenario(s) | <!-- e.g. extensions/molecule/integration_satellite_content_view_create --> |
| Other | <!-- e.g. scripts/verify_readme.py, .github/workflows/main.yml --> |

## Test plan

<!-- Describe how you validated this change. Check all that apply. -->

- [ ] Reviewed diff locally
- [ ] `ansible-lint` passes (if Ansible content changed)
- [ ] README format check passes (if a role README changed):

  ```bash
  python scripts/verify_readme.py roles/<role>/README.md \
    --template docs/templates/role_readme_format_template.md
  ```
  - [ ] Security scan passed if a role was updated

  ```bash
  python3 scripts/security_checks.py roles/<role_name>
  ```

- [ ] Molecule scenario run (if applicable):

  ```bash
  cd extensions/molecule
  ln -sfn . molecule
  molecule test -s <scenario>
  ```

- [ ] CI checks pass on this PR

**Notes / commands run:**

<!-- Paste relevant command output or manual test steps. -->

## Release notes

<!-- Optional user-facing note for a changelog entry. Leave blank if not applicable. -->

-

## Checklist

- [ ] Role README follows `docs/templates/role_readme_format_template.md` (for role changes)
- [ ] Discussed with the team (for new roles or significant design changes)
- [ ] No secrets, credentials, or environment-specific values committed
- [ ] Breaking changes or migration steps documented above (if any)
