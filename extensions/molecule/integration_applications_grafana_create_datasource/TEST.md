# TEST: integration_applications_grafana_create_datasource

## Purpose

Validate extension-level Molecule scenario wiring for
`infra.ado.applications_grafana_create_datasource`.

## Sequence

- `prepare`
- `converge`
- `idempotence`
- `verify`
- `destroy`

## Notes

- `prepare` and `destroy` are no-op safe.
- `verify` confirms role README presence.
- `converge` supports optional live execution when
  `APPLICATIONS_GRAFANA_CREATE_DATASOURCE_ENABLE_LIVE_CHECKS=true`.

## Run

```bash
cd extensions/molecule
molecule test -s integration_applications_grafana_create_datasource
```
