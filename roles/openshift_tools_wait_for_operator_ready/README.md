---

## `status_message`

**Example Usage:**

```yaml
- name: Execute the status_message role
  hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift_infrastructure_automation.status_message
      vars:
        example_variable: example_value
```

> Replace `example_variable` and `example_value` with the appropriate parameters defined in `defaults/main.yml` for the role.


**Description**: Emits status message for GitOps/audit flows

**Structure:**
```
status_message/
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