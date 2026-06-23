# Test Plan — `ocp_compliance_install`

This document describes how to validate the role-local Molecule scenario for
`ocp_compliance_install`.

## Prerequisites

- OpenShift/Kubernetes cluster reachable.
- `K8S_AUTH_*` exported (or kubeconfig-based auth configured).
- Required collection installed:
  - `ansible-galaxy collection install kubernetes.core`

## Default behavior

By default, `molecule/default/converge.yml` skips live API checks so Molecule
can run safely in non-cluster environments.

## Live-check execution

Enable real cluster validation:

```bash
export OCP_COMPLIANCE_INSTALL_ENABLE_LIVE_CHECKS=true
export OCP_COMPLIANCE_INSTALL_OPERATOR_NAMESPACE=openshift-compliance
molecule test
```

## Expected result

- The role queries pods in the configured namespace.
- Molecule verify validates README format using
  `scripts/verify_readme.py` and the role README template.

## Useful commands

```bash
molecule converge
molecule idempotence
molecule verify
molecule destroy
```
