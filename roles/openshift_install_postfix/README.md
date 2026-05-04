# Role: ado.openshift.postfix

Deploy and test a Postfix mail relay server in OpenShift.

---

## Features

- Creates a dedicated namespace for Postfix (`postfix_namespace`, default: `postfix-relay`).
- Sets up a Kubernetes Secret for SMTP relay authentication credentials.
- Configures Postfix using a ConfigMap for `main.cf`.
- Deploys a Pod running Postfix and required packages.
- Exposes the Pod as a Service for SMTP (port 25).
- Optionally sends a test email from the Pod.
- Includes optional cleanup of the test Pod after sending.

---

## Requirements

- OpenShift or Kubernetes cluster reachable with authentication (`K8S_AUTH_*` environment variables or module params).
- Collections:
  - `kubernetes.core`
- SMTP relay credentials.
- The container (default: UBI9) must permit package installs and running as root.
- For test email, the relay credentials must be valid and permitted.

---

## Variables

| Variable            | Default                                 | Description                                     |
|---------------------|-----------------------------------------|-------------------------------------------------|
| `postfix_namespace` | `postfix-relay`                         | Namespace to deploy resources.                   |
| `postfix_image`     | `registry.access.redhat.com/ubi9/ubi`   | Container image for the Postfix Pod.             |
| `smtp_user`         | —                                       | SMTP relay username.                             |
| `smtp_password`     | —                                       | SMTP relay password.                             |
| `relay_host`        | `smtp.gmail.com`                        | SMTP relay host.                                 |
| `test_email`        | `test@example.com`                      | From address for test message.                   |
| `recipient_email`   | `chelliot@redhat.com`                   | Recipient for test message.                      |

---

## Examples

### Minimal

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.postfix
      vars:
        smtp_user: "myuser"
        smtp_password: "mypassword"
```

### Custom relay and recipient

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.postfix
      vars:
        smtp_user: "myuser"
        smtp_password: "mypassword"
        relay_host: "smtp.office365.com"
        test_email: "sender@example.com"
        recipient_email: "receiver@example.com"
```

---

## Outputs

- Shows service details (ClusterIP, NodePort).
- Sends a test email and displays Pod output.
- Pod is deleted after test (override or remove cleanup task to persist Pod).

---

## Behavior Notes

- Postfix configuration and credentials are provided using ConfigMap and Secret, mounted into the Pod.
- The Pod installs Postfix and starts it in foreground.
- Service exposes SMTP on NodePort.
- Pod runs as root for broad compatibility.
- For persistent deployment, remove or comment cleanup task at the end of `tasks/main.yml`.

---

## Troubleshooting

- If the Pod fails to start, check Pod logs for package install or Postfix errors.
- Ensure the relay host and credentials are correct and permitted.
- NodePort may not be reachable outside the cluster without additional networking setup.
- For TLS relay hosts, make sure CA certificates are available in the container.

---

## Molecule

A default Molecule scenario is provided under `molecule/default` and covers:
- Namespace and resource creation.
- Secret and ConfigMap content.
- Pod lifecycle and email test.
- Service exposure and cleanup.

Set kube auth via environment:

```bash
export K8S_AUTH_HOST="https://api.ocp.example:6443"
export K8S_AUTH_API_KEY="…"
export K8S_AUTH_VERIFY_SSL="no"
```

Run:

```bash
molecule converge
molecule idempotence
molecule verify
molecule destroy
```

Your `molecule.yml` wires `converge`, `verify`, and `destroy` to their respective playbooks.

---

## Author

- Chad Elliott (<chelliot@redhat.com>)

---

## Repository layout

```text
.
├── defaults
│   └── main.yml
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── molecule
│   └── default
│       ├── converge.yml
│       ├── destroy.yml
│       ├── molecule.yml
│       ├── README.md
│       ├── TEST.md
│       └── verify.yml
├── README.md
├── tasks
│   └── main.yml
├── tests
│   ├── inventory
│   └── test.yml
└── vars
    └── main.yml
```