---

## `advanced-cluster-management`

**Example Usage:**

```yaml
- name: Execute the advanced-cluster-management role
  hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift_infrastructure_automation.advanced-cluster-management
      vars:
        example_variable: example_value
```

> Replace `example_variable` and `example_value` with the appropriate parameters defined in `defaults/main.yml` for the role.


**Description**: Installs and configures Red Hat ACM operator and CRDs

**Structure:**
```
advanced-cluster-management/
├── defaults/main.yml
├── vars/main.yml
├── tasks/main.yml
├── templates/
├── handlers/main.yml
├── files/
├── tests/
│   ├── inventory
│   └── test.yml
└── README.md
```