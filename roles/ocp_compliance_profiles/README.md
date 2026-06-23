# Role: `ocp_compliance_profiles`

Create or delete a Compliance Operator `ComplianceProfile` resource.

## Role Author

Chad Elliott

## ✅ Role Requirements

- OpenShift/Kubernetes API access.
- `kubernetes.core` collection installed.
- Compliance Operator CRDs installed in the target cluster.

## 📦 Role Variables

| Variable | Description | Required | Default |
| -------- | ----------- | -------- | ------- |
| `ocp_compliance_profiles_manage_profile` | Action selector. Use `create` or `delete`. | No | `create` |
| `ocp_compliance_profiles_profile` | ComplianceProfile resource name. | Yes | `""` |
| `ocp_compliance_profiles_profile_title` | Human-readable title used when creating the profile. | Yes* | `""` |
| `ocp_compliance_profiles_profile_description` | Description used when creating the profile. | Yes* | `""` |
| `ocp_compliance_profiles_operator_namespace` | Namespace for ComplianceProfile resources. | No | `openshift-compliance` |

> **Notes:**
> \* Required when `ocp_compliance_profiles_manage_profile` is `create`.

## 🚀 Role Usage

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_compliance_profiles
      vars:
        ocp_compliance_profiles_manage_profile: create
        ocp_compliance_profiles_profile: custom-hardening
        ocp_compliance_profiles_profile_title: Custom Hardening Profile
        ocp_compliance_profiles_profile_description: Site-specific compliance profile
        ocp_compliance_profiles_operator_namespace: openshift-compliance
```

## 🧪 Role Molecule Testing

This role has two Molecule paths:

- Role-local scenario at `roles/ocp_compliance_profiles/molecule/default`.
  - Uses local `converge.yml` and `destroy.yml`.
  - Default flow is `dependency -> create -> converge -> idempotence -> destroy -> verify`.
- Extension-level scenario at `extensions/molecule/integration_ocp_compliance_profiles`.
  - Uses shared playbooks:
    - `extensions/molecule/utils/playbooks/ocp_compliance_profiles_prepare.yml`
    - `extensions/molecule/utils/playbooks/ocp_compliance_profiles_converge.yml`
    - `extensions/molecule/utils/playbooks/ocp_compliance_profiles_verify.yml`
    - `extensions/molecule/utils/playbooks/ocp_compliance_profiles_destroy.yml`
  - Flow is `prepare -> converge -> idempotence -> verify` with `destroy` in `destroy_sequence`.

Run the extension scenario from `extensions/molecule`:

```bash
molecule test -s integration_ocp_compliance_profiles
```

To run live checks in extension converge, enable:

```bash
export OCP_COMPLIANCE_PROFILES_ENABLE_LIVE_CHECKS=true
```

## 📁 Role Structure

```text
ocp_compliance_profiles/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── molecule/
│   └── default/
│       ├── converge.yml
│       ├── destroy.yml
│       ├── molecule.yml
│       ├── README.md
│       ├── TEST.md
│       └── verify.yml
├── README.md
├── tasks/
│   └── main.yml
├── tests/
│   ├── inventory
│   ├── roles/
│   │   └── ocp_compliance_profiles
│   └── test.yml
└── vars/
    └── main.yml
```
