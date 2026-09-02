# Role: infra.ado.ocp_virtualization

Provision an OpenShift Virtualization VM from a cluster **DataSource** / DV
(for example the built-in `rhel9` image in `openshift-virtualization-os-images`),
with optional Multus bridge networking and cloud-init.

VM creation is delegated to validated
[`infra.openshift_virtualization_ops.vm_provision`](https://github.com/redhat-cop/openshift_virtualization_ops).
This role builds the lab-specific VirtualMachine spec (DataSource
`dataVolumeTemplates`, Multus NAD, cloud-init, instance type / preference).

## Role Author

Automation Development Office

## ✅ Role Requirements

- OpenShift Virtualization (KubeVirt) installed
- Collections: `kubernetes.core`, `infra.openshift_virtualization_ops`
  (Automation Hub validated / GitHub; not on public Galaxy)
- OpenShift credentials via `K8S_AUTH_*` or `provision_openshift_virt_api_*` /
  `host` + `token` (mapped into `vm_provision_*`)
- A usable DataSource (prefer provided golden images: `rhel9`, `rhel8`, …)

## 📦 Role Variables

| Variable | Description |
|----------|-------------|
| `source_name` | Cluster DataSource name (default `rhel9`) |
| `source_namespace` | DataSource namespace (default `openshift-virtualization-os-images`) |
| `instance_type` | KubeVirt instance type (default `u1.large`, 2 CPU / 8Gi) |
| `preference` | Guest preference (default `rhel.9`) |
| `vm_namespace` | Target namespace (default `ado-built-vm`) |
| `vm_name` | VirtualMachine metadata.name (required) |
| `network_mode` | `pod` or `bridge` (use with `multus_network_name` for br-ex) |
| `vm_state` | `present` or `absent` (absent deletes VM locally) |

`vm_provision` creates only when the VM is missing — it does not patch an existing
VirtualMachine.

## 🚀 Role Usage

```yaml
- name: Provision Virt VM
  hosts: localhost
  gather_facts: false
  roles:
    - role: infra.ado.ocp_virtualization
      vars:
        vm_name: keycloak-ado
        vm_namespace: ado-built-vm
        source_name: rhel9
        instance_type: u1.large
        preference: rhel.9
        network_mode: bridge
        multus_network_name: ado-built-vm/br-ex-network
```

Contoller playbook: `playbooks/provision/ado-provision-openshift-virt-vm-bootstrap.yml`
JT: **ADO | Provision OpenShift Virt VM**. Survey / extra_vars should win over
stale `component_config` defaults.

If the VMI shows `ErrorUnschedulable` with `Insufficient memory`, shrink the
instance type rather than changing the guest image.

## 🧪 Role Molecule Testing

No Molecule scenario ships with this role yet. Validate via Contoller JT
`ado-ocp-virtualization-deploy-bootstrap` or lab virt provision workflow.

## 📁 Role Structure

```text
roles/ocp_virtualization/
  README.md
  defaults/main.yml
  meta/main.yml
  tasks/
    main.yml
    create_vm.yml
    delete_vm.yml
```
