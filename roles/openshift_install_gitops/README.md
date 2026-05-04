# Role: openshift_install_gitops

Apply an Argo CD instance and optionally enforce a route for OpenShift GitOps.

---

## Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- Argo CD / OpenShift GitOps operator installed before this role runs.

---

## Variables

| Variable | Description |
|---------|-------------|
| `app_namespace` | Namespace where Argo CD pods are expected to run. Required for pod waiting. |
| `name_space` | Namespace used when enforcing a route if it differs from `app_namespace`. |
| `argocd_name` | Argo CD resource name. Defaults to `openshift-gitops`. |
| `argocd_namespace` | Namespace used for the `ArgoCD` custom resource. |
| `route_enforce` | Boolean toggle for explicit route management. |
| `route_name / route_hostname / route_termination` | Route customization variables when `route_enforce` is enabled. |

---

## Examples

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: openshift_install_gitops
      vars:
        app_namespace: openshift-gitops
        argocd_name: openshift-gitops
        argocd_namespace: openshift-gitops
        route_enforce: true
        route_hostname: gitops.apps.example.com
```

---

## Behavior Notes

- Creates an `ArgoCD` custom resource and waits for pods by including the shared wait role.
- Optionally creates or updates the GitOps route and prints the resolved URL.

---

## Molecule

Use the same README layout as the working collection roles so Molecule/README validation sees the expected sections and ordering.

```
dependency -> lint -> syntax -> create -> converge -> idempotence -> destroy -> verify
```

---

## License

GPL-3.0-or-later

---

## Author

Chad Elliott

---

## Repository layout (role)

```text
roles/
`-- openshift_install_gitops/
    |-- README.md
    |-- defaults/
    |   `-- main.yml
    |-- tasks/
    |   `-- main.yml
    |-- vars/
    |   `-- main.yml
    |-- handlers/
    |   `-- main.yml
    |-- meta/
    |   `-- main.yml
    |-- templates/                # optional
    |-- files/                    # optional
    `-- tests/
        |-- inventory
        `-- test.yml               # optional
```
