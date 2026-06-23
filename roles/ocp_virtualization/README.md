## `ocp_virt`

This role provisions and starts a VirtualMachine (VM) in OpenShift Virtualization by cloning an existing DataVolume or DataSource. It configures storage, networking, and cloud-init, and ensures the VM is running.

---

### ✅ Role Requirements

- Access to an OpenShift cluster with OpenShift Virtualization enabled.
- The `redhat.openshift_virtualization` Ansible collection must be installed.
- Cluster access credentials should be provided via `KUBECONFIG` or environment variables.

---

### 📦 Role Variables

| Variable                | Description                                                                 | Required | Default                                      |
|-------------------------|-----------------------------------------------------------------------------|----------|----------------------------------------------|
| `vm_name`               | Name of the VirtualMachine                                                  | ✅       | —                                            |
| `vm_namespace`          | Namespace for the VirtualMachine                                            | ✅       | —                                            |
| `source_name`           | Name of the source DataVolume/DataSource to clone                           | ✅       | —                                            |
| `storage_class`         | Storage class for the cloned DataVolume                                     | ✅       | —                                            |
| `instance_type`         | Instance type for the VM                                                    | ✅       | —                                            |
| `storageclass`          | StorageClass name for VM storage                                            | ✅       | —                                            |
| `cloud_init_user_data`  | Cloud-init user data for VM initialization                                  | ✅       | —                                            |
| `app_label`             | Label for the VM (defaults to `vm_name`)                                    |          | `vm_name`                                    |
| `preference`            | VM preference                                                               |          | `rhel.9`                                     |
| `source_kind`           | Kind of source to clone (`DataSource` or `DataVolume`)                      |          | `DataSource`                                 |
| `source_namespace`      | Namespace of the source image                                               |          | `openshift-virtualization-os-images`         |
| `wait_timeout`          | Timeout (seconds) to wait for VM to be ready                                |          | `3600`                                       |
| `network_name`          | Name of the network interface                                               |          | `default`                                    |

---

### **Example Usage**

```yaml
- name: Create a RHEL9 VM from a DataSource
  hosts: localhost
  gather_facts: false
  vars:
    vm_name: rhel9-vm
    vm_namespace: default
    source_name: rhel9-image
    storage_class: ocs-storagecluster-ceph-rbd
    instance_type: u1.medium
    cloud_init_user_data: |
      #cloud-config
      password: mypassword
      chpasswd: { expire: False }
  roles:
    - role: ocp_virt
```

---

### **Structure**
```
ocp_virt/
├── defaults/main.yml
├── vars/main.yml
├── tasks/
│   ├── main.yml
│   └── create_vm.yml
├── templates/
├── handlers/main.yml
├── files/
├── tests/
│   ├── inventory
│   └── test.yml
└──
```