---

## `Kube Descheduler Operator Role`
**Description**: Configures a Kube Descheduler object with user defined Descheduler profiles

**Example Usage:**

```yaml
- name: Execute the Kube Descheduler role
  hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift.kube-descheduler
  vars:
    kube_descheduler_state: present
    instance_name: cluster
    scheduling_interval: 300
    descheduler_profiles:
      - AffinityAndTaints
      - TopologyAndDuplicates

```

**Kube-descheduler must be installed, an example install playbook is as follows:**

> To run this playbook, you will need access to the Openshift ADO collections

```yaml
---
- name: Deploy Kube Descheduler
  hosts: localhost
  gather_facts: false
  collections: ado:openshift

  vars_files:
     - vault.yml

  vars:
    # namespace vars
    name_space: openshift-kube-descheduler-operator
    all_namespaces_install: false
    state: present
    # operator OperatorGroup
    operatorgroup: openshift-operators-redhat
    # subscription_operator
    operator_name: cluster-kube-descheduler-operator
    operator_channel: stable
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
kube_descheduler_state: (present or absent) ## This specifies whether to create the Kube Descheduler object assuming Kube-Descheduler is installed
instance_name: (string value, e.g. instance) ## This is the name you are giving your Kube Descheduler profile
scheduling_interval: (time in seconds) ## This specifies the waiting interval before scheduling a pod to a new node based on the profiles you have configured.
descheduler_profiles: (example options below) ## These are the different profiles that can be set, note that not all are compatible. Refer to Kube-Descheduler documentation for details on profiles
  - AffinityAndTaints
  - TopologyAndDuplicates
  - SoftTopologyAndDuplicates
  - LifecycleAndUtilization
  - LongLifecycle
  - CompactAndScale
  - EvictPodsWithPVC
  - EvictPodsWithLocalStorage
```

**Structure:**
```
kube-descheduler/
├── defaults/main.yml
├── vars/main.yml
├── tasks/
│   ├── main.yml
│   ├── kube-descheduler.yml
├── templates/
├── handlers/main.yml
├── files/
├── meta/main.yaml
├── tests/
│   ├── inventory
└── README.md
```