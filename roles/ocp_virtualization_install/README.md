# Role: infra.ado.ocp_virtualization_install

Install and wait for the OpenShift Virtualization (CNV / HyperConverged)
operator on an OpenShift cluster.

## Role Author

Automation Development Office

## Requirements

- OpenShift API access (`kubernetes.core`)
- OperatorHub catalog access for `kubevirt-hyperconverged`

## Role Variables

| Variable | Description |
|----------|-------------|
| `name_space` / `operator_namespace` | Target namespace (typically `openshift-cnv`) |
| `operator_name` | Subscription package name |
| `operator_name_substring` | CSV / deployment match string |

## Example

```yaml
- hosts: localhost
  roles:
    - role: infra.ado.ocp_virtualization_install
```

## License

See collection LICENSE.
