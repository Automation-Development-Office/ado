--

## `Openshift Data Foundation Operator Role`
**Description**: Configures Openshift Data Foundation initial storage cluster

**Example Usage:**

```yaml
- name: Execute the Openshift Data Foundation role
  hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.openshift_data_foundation
  vars:
    storage_cluster_name: ben-ocs
    resource_profile: lean
    storage_system_size: ".5Ti"
    storage_class: "gp3-csi"
    nfs_enabled: false

```

**Openshift Data Foundation must be installed, an example install playbook is as follows:**

> To run this playbook, you will need access to the Openshift ADO collections

```yaml
---
- name: Deploy Openshift Data Foundation Operator
  hosts: localhost
  gather_facts: false
  collections: ado:openshift

  vars_files:
     - vault.yml

  vars:
    # namespace vars
    name_space: openshift-storage
    all_namespaces_install: false
    state: present
    # operator OperatorGroup
    operatorgroup: openshift-storage
    # subscript_operator
    operator_name: odf-operator
    operator_channel: stable-4.19
    operator_source: redhat-operators
    operator_source_namespace: openshift-marketplace

  roles:
    - role: ado.openshfit.namespace       
    - role: ado.openshift.operatorgroup
    - role: ado.openshift.subscription_operator
    - role: ado.openshift.wait_for_pods_running
```

**Required Variables**
```
storage_cluster_name: "string" ## This is the intended name for the storage cluster you are creating, note this will create similarly named storage classes.
resource_profile: "lean/balanced/performance" ## This is the level of performance for the Openshift Data Foundation cluster, guidelines are as follows:
    Lean: This profile is designed for resource-constrained environments. It minimizes resource consumption by allocating fewer CPUs and less memory than the other profiles. It is suitable when resources are lower than recommended specifications.
    Example: 24 CPU, 72 GiB RAM (these values can vary slightly depending on the ODF version and specific deployment).
    Balanced (Default): This profile provides a balance between resource consumption and performance. It is the default choice and is recommended when the recommended resources are available, offering a good balance for diverse workloads. 
    Example: 30 CPU, 72 GiB RAM.
    Performance: This profile is tailored for high-performance environments with ample resources. It allocates more memory and CPUs to ensure optimal execution of demanding workloads, providing the best possible performance. 
    Example: 45 CPU, 96 GiB RAM.
storage_system_size: ".5Ti/1Ti/2Ti..." ## This is the size that you desire for the end storage state.
## VERY IMPORTANT NOTE REGARDING storage_system_size
## The number defined by storage_system_size is the amount of storage allotted to each node in the storage cluster. Thus if you pick .5Ti, and you have 3 nodes, you are actually going to provision .5Ti on each of the 3 nodes, and will total 1.5 Ti across the whole cluster. This is to ensure data replication and reliability.
storage_class: "storage class name" ## This should be an existing storage class for your cluster, I have been using gp3-csi on AWS
nfs_enabled: true/false ## This is specifying whether an NFS storage class should be provisioned.
```

**Structure:**
```
openshift_data_foundation/
├── defaults/main.yml
├── vars/main.yml
├── tasks/
│   ├── main.yml
│   ├── storage_cluster.yml
├── templates/
├── handlers/main.yml
├── files/
├── meta/main.yaml
├── tests/
│   ├── inventory
└── README.md
```