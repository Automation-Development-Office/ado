---

## `iscsi-storage`

**Example Usage:**

```yaml
- name: Execute the iscsi-storage role
  hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift_infrastructure_automation.iscsi-storage
      vars:
        example_variable: example_value
```

> Replace `example_variable` and `example_value` with the appropriate parameters defined in `defaults/main.yml` for the role.


**Description**: Configures default iSCSI storage class

**Structure:**
```
iscsi-storage/
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