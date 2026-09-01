# Role: infra.ado.ocp_default_ingress_cert

Replace the OpenShift default IngressController TLS certificate (router
wildcard for `*.apps.<domain>`) and optionally trust the issuing CA
cluster-wide via `Proxy/cluster` `trustedCA`.

## Role Author

Automation Development Office

## Requirements

- OpenShift API access (`kubernetes.core`)
- PEM certificate and private key for the wildcard (or SAN) cert

## Role Variables

| Variable | Description |
|----------|-------------|
| `tls_crt` / `tls_key` | Router wildcard certificate and key (PEM) |
| `ca_crt` | Optional issuing CA / chain PEM |
| `ocp_default_ingress_trust_ca_clusterwide` | When true, ConfigMap + Proxy trustedCA |

## Example

```yaml
- hosts: localhost
  roles:
    - role: infra.ado.ocp_default_ingress_cert
```

## License

See collection LICENSE.
