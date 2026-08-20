# Role: infra.ado.ocp_virtualization

Provision an OpenShift Virtualization VM from a cluster **DataSource** / DV
(for example the built-in `rhel9` image in `openshift-virtualization-os-images`),
with optional Multus bridge networking and cloud-init.

## Requirements

- OpenShift Virtualization (KubeVirt) installed
- `kubernetes.core` / OpenShift credentials via `K8S_AUTH_*`
- A usable DataSource (prefer provided golden images: `rhel9`, `rhel8`, …)

## Defaults (lab-friendly)

| Variable | Default | Notes |
|----------|---------|--------|
| `source_name` | `rhel9` | Cluster DataSource — do not reinvent guest images |
| `source_namespace` | `openshift-virtualization-os-images` | |
| `instance_type` | `u1.large` | **2 CPU / 8Gi** — `u1.xlarge` (~16Gi) often hits `ErrorUnschedulable` on busy workers |
| `preference` | `rhel.9` | |
| `vm_namespace` | `ado-built-vm` | Created via `infra.ado.ocp_namespace` when wired that way |

## Contoller

Playbook: `playbooks/provision/ado-provision-openshift-virt-vm-bootstrap.yml`  
JT: `ADO | Provision OpenShift Virt VM`

Survey / extra_vars should win over stale `component_config` satellite-server defaults.

## Example

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

## Scheduling tip

If the VMI shows `ErrorUnschedulable` with `Insufficient memory`, shrink the
instance type (for example `u1.large` or `u1.2xmedium`) rather than changing the
guest image. The DataSources already provide RHEL.
