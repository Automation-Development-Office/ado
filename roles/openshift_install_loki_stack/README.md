---

## `Loki Stack Operator Role`
**Description**: Configures a Loki Stack
**Example Usage:**

```yaml
- name: Deploy Loki Stack
  hosts: localhost
  gather_facts: false
  collections: ado:openshift_infrastructure_automation

  vars_files:
     - vault.yml

  vars:
    # loki vars
    loki_stack_state: present
    loki_name: lokistack
    loki_secret: loki-secret
    loki_storage_type: s3
    loki_size: 1x.demo
    loki_storage_class_name: gp3-csi

  roles:
    - role: ado.loki-stack
```

**The Loki Operator must be installed, an example install playbook is as follows:**

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
    name_space: openshift-operators-redhat
    all_namespaces_install: true
    state: absent
    # operator OperatorGroup
    operatorgroup: openshift-operators-redhat
    # subscription_operator
    operator_name: loki-operator
    operator_channel: stable-6.3
    operator_source: redhat-operators
    operator_source_namespace: openshift-marketplace

  roles:
    - role: ado.openshift.namespace       
    - role: ado.openshift.operatorgroup
    - role: ado.openshift.subscription_operator
    - role: ado.openshift.wait_for_pods_running
```

**Required Variables**
```
  loki_stack_state: (present or absent) ## This specifies whether to create the a Loki Stack object assuming Loki Operator is installed
  loki_name: (string, e.g. loki_stack)  ## This specifies the name of the Loki Stack object
  loki_secret: (string)  ## This specifies the secret name required for loki
  loki_storage_type: (string) ## Specifies backing storage type for Loki stack
  loki_size: (string, e.g. 1x.demo) ## The size of the Loki Stack, see Loki documentation for more details.
  loki_storage_class_name: (string) ## Specifiy Openshift Storage class that is being utilized.
```

**Required Environmentals**
> This version of the role assumes you already have a loki secret configured, future update of this role will try to get rid of that requirement. A sample secret follows:

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: <secret-name>
  namespace: <loki-namepspace>
data:
  access_key_id: <s3 access key id>
  access_key_secret: <s3 access key secret>
  bucketnames: <s3 bucketname>
  endpoint: <s3 endpoint>
```

**Structure:**
```
loki-stack/
├── defaults/main.yml
├── vars/main.yml
├── tasks/
│   ├── main.yml
│   ├── loki-stack.yml
├── templates/
├── handlers/main.yml
├── files/
├── meta/main.yaml
├── tests/
│   ├── inventory
└── README.md
```
