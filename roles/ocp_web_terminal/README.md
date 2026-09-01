# Role: infra.ado.ocp_web_terminal

Install and wait for the OpenShift Web Terminal operator.

## Role Author

Automation Development Office

## Requirements

- OpenShift API access (`kubernetes.core`)
- OperatorHub catalog access for `web-terminal`

## Role Variables

| Variable | Description |
|----------|-------------|
| `name_space` / `operator_namespace` | Operator namespace |
| `operator_name` | Subscription package name |
| `operator_name_substring` | CSV / deployment match string |

## Example

```yaml
- hosts: localhost
  roles:
    - role: infra.ado.ocp_web_terminal
```

## License

See collection LICENSE.
