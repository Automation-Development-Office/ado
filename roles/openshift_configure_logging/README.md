---

## `Openshift Logging  Role`
**Description**: Configures a Cluster Forwarder object for Openshift Logging

**Example Usage:**

```yaml
- name: Deploy Openshift Cluster Forwarder
  hosts: localhost
  gather_facts: false
  vars:
    cluster_forwarder_state: present
    cluster_forwarder_name: instance
    cluster_forwarder_secret_key: name-of-secret-key
    cluster_forwarder_secret: vector-splunk-secret
    splunk_url: https://fake-splunk.fqdn
    splunk_logging_name: splunk-aud
    splunk_secret: test123
  roles:
    - role: ado.openshift.openshift-logging

```

**Openshift Logging must be installed, an example install playbook is as follows:**

> To run this playbook, you will need access to the Openshift ADO collections

```yaml
---
- name: Deploy Openshift Logging
  hosts: localhost
  gather_facts: false
  collections: ado:openshift

  vars_files:
     - vault.yml

  vars:
    # namespace vars
    name_space: openshift-logging
    all_namespaces_install: true
    state: present
    # operator OperatorGroup
    operatorgroup: global-operators
    # subscript_operator
    operator_name: cluster-logging
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
    cluster_forwarder_state: (present or absent) ## Specifies if you want to install the cluster forwarder
    cluster_forwarder_name: (string) ## Specifies the name of your Cluster Forwarder instance.
    cluster_forwarder_secret_key: (string) ## Name of the secret key value in your secret
    cluster_forwarder_secret: (string) ## Name of your Openshift secret object
    splunk_url: (url) ## Specifies what splunk server you want to forward logs too
    splunk_logging_name: (string) ## Name of your Splunk logging 
```

**Required Environmentals**
> You must specify the cluster_forwarder_secret to reference the name of the secret you want to utilize, but if you haven't defined a secret, you can define the splunk_secret variable with the appropriate secret value, and the playbook will create the secret for you.

 

**Structure:**
```
openshift-logging/
├── defaults/main.yml
├── vars/main.yml
├── tasks/
│   ├── main.yml
│   ├── cluster-forwarder.yml
├── templates/
├── handlers/main.yml
├── files/
├── meta/main.yaml
├── tests/
│   ├── inventory
└── README.md
```