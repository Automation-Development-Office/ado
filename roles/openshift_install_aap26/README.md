---

## `cert-manager`

**Example Usage:**

```yaml
- name: Execute the cert-manager role
  hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift_infrastructure_automation.cert-manager
      vars:
        example_variable: example_value
```

> Replace `example_variable` and `example_value` with the appropriate parameters defined in `defaults/main.yml` for the role.


**Description**: Installs cert-manager and integrates with external CA

**Structure:**
```
cert-manager/
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