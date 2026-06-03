# TEST: integration_grafana_manage_folders

## Purpose

Validate extension-level Molecule scenario wiring for
`infra.ado.grafana_manage_folders`.

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
  `GRAFANA_MANAGE_FOLDERS_ENABLE_LIVE_CHECKS=true`.

## Run

```bash
cd extensions/molecule
molecule test -s integration_grafana_manage_folders
```
