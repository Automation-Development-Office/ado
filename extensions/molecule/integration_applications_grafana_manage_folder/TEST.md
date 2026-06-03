# TEST: integration_applications_grafana_manage_folder

## Purpose

Validate extension-level Molecule scenario wiring for
`infra.ado.applications_grafana_manage_folder`.

## Sequence

- `prepare`
- `converge`
- `idempotence`
- `verify`
- `destroy`

## Notes

- `prepare` and `destroy` are no-op safe steps.
- `verify` confirms role README presence.
- `converge` supports optional live execution when
  `APPLICATIONS_GRAFANA_MANAGE_FOLDER_ENABLE_LIVE_CHECKS=true`.

## Run

```bash
cd extensions/molecule
molecule test -s integration_applications_grafana_manage_folder
```
