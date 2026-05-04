# Role: ado.openshift_infrastructure_automation.gitlab_runner

This role deploys GitLab Runner to an OpenShift cluster using a Kubernetes Deployment manifest. It registers the runner with GitLab and sets up the namespace and service account needed to operate.

## Variables

| Name         | Description                         | Required | Default |
|--------------|-------------------------------------|----------|---------|
| namespace    | Namespace to deploy into            | No       | gitlab-runner |
| runner_name  | Display name of the GitLab runner   | No       | openshift-runner |
| gitlab_url   | GitLab server URL                   | Yes      | https://gitlab.com/ |
| runner_token | GitLab runner registration token    | Yes      | "" |
| image        | GitLab Runner image to deploy       | No       | gitlab/gitlab-runner:alpine |

## Example

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: ado.openshift_infrastructure_automation.gitlab_runner
      vars:
        gitlab_url: "https://gitlab.com/"
        runner_token: "{{ vault_gitlab_runner_token }}"
```
