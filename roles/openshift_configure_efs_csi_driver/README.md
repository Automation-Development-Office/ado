--

## `AWS CSI Driver Role`
**Description**: Configures AWS CSI Driver storage class

**Example Usage:**

```yaml
- name: Execute the AWS CSI Driver role
  hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.efs_csi_driver
  vars:
    base_path: '/drive_name'
    base_path_perms: '700'
    efs_filesystem_id: fsid_01010101
    gid_end: '2000'
    gid_start: '1000'
    reclaim_policy: 'Delete'
    binding_mode: 'Immediate'
    storage_class_name: 'efs-sc'
    state: 'present'

```

**AWS EFS CSI Driver must be installed, an example install playbook is as follows:**

> To run this playbook, you will need access to the Openshift ADO collections

```yaml
---
- name: Deploy AWS CSI Driver
  hosts: localhost
  gather_facts: false
  collections: ado:openshift

  vars_files:
     - vault.yml

  vars:
    # namespace vars
    name_space: openshift-cluster-csi-drivers
    all_namespaces_install: true
    state: present
    # subscript_operator
    operator_name: aws-efs-csi-driver-operator
    operator_channel: stable
    operator_source: redhat-operators
    operator_source_namespace: openshift-marketplace

  roles:
    - role: ado.openshfit.namespace       
    - role: ado.openshift.subscription_operator
    - role: ado.openshift.wait_for_pods_running
```

**Required Variables**
```
base_path: '/drive_name' # This is the base path specification for your EFS filesystem
base_path_perms: '700' # This is the permissions for your EFS base path
efs_filesystem_id: fsid_<number> # This is the fsid number of the EFS filesystem that has been created in AWS. Future work could be done to automate creation of this filesystem.
gid_end: '<gid_number>' # The max gid number for access to this filesystem
gid_start: '<gid_number>' # The min gid number for access to this filesystem
reclaim_policy: 'Delete|Retain' # Whether storage should be retained or deleted when no longer in use by Openshift
binding_mode: 'Immediate|WaitForFirstConsumer' # Specifies whether a PV is provisioned immediately when a PVC is created or if it will wait for something to use it before provisioning
storage_class_name: 'efs-sc' # The name you want for your EFS Storage Class
state: 'present|absent' # Specifies whether you are creating or deleting the storage class.
```

**Structure:**
```
efs_csi_driver/
├── defaults/main.yml
├── vars/main.yml
├── tasks/
│   ├── main.yml
│   ├── storage_class.yml
├── templates/
├── handlers/main.yml
├── files/
├── meta/main.yaml
├── tests/
│   ├── inventory
└── README.md
```