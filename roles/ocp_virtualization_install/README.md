# Role: infra.ado.ocp_virtualization_install

Install and wait for the OpenShift Virtualization (CNV / HyperConverged)
operator on an OpenShift cluster.

## Role Author

Automation Development Office

## ✅ Role Requirements

- OpenShift API access (`kubernetes.core`)
- OperatorHub catalog access for `kubevirt-hyperconverged`

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `name_space` / `operator_namespace` | Target namespace (typically `openshift-cnv`) |
| `operator_name` | Subscription package name |
| `operator_name_substring` | CSV / deployment match string |

## 🚀 Role Usage

```yaml
- hosts: localhost
  roles:
    - role: infra.ado.ocp_virtualization_install
```

## 🧪 Role Molecule Testing

No Molecule scenario ships with this role yet. Validate via the OpenShift
**Deploy OpenShift Virtualization** JT after bootstrap.

## 📁 Role Structure

```text
roles/ocp_virtualization_install/
  README.md
  defaults/main.yml
  meta/main.yml
  tasks/main.yml
```
