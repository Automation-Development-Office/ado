# fakecloud for AWS API tests

Some Molecule scenarios exercise real AWS SDK calls (modules, roles, or
playbooks). CI starts [fakecloud](https://fakecloud.dev/) only for scenarios
listed in `fakecloud_scenarios.txt` — other scenarios are unchanged.

## Opt in a scenario

1. Add the scenario name (basename of `extensions/molecule/<name>/`) to
   `extensions/molecule/fakecloud_scenarios.txt`.
2. Point tests at fakecloud with dummy credentials and the local endpoint:
   - `AWS_ACCESS_KEY_ID=test`
   - `AWS_SECRET_ACCESS_KEY=test`
   - `AWS_ENDPOINT_URL=http://127.0.0.1:4566`
3. Install any AWS collection dependencies in the scenario `requirements.yml`
   (for example `amazon.aws`).

## Local run

```bash
# Terminal 1
scripts/ci/fakecloud-service.sh start

# Terminal 2
source scripts/ci/fakecloud-env.sh
ansible-galaxy collection install . --force --no-deps -p ~/.ansible/collections
ansible-galaxy collection install -r extensions/molecule/integration_ec2_ami_copy/requirements.yml \
  -p ~/.ansible/collections
export ANSIBLE_COLLECTIONS_PATH="$HOME/.ansible/collections"
cd extensions/molecule && ln -sfn . molecule
molecule test -s integration_ec2_ami_copy

scripts/ci/fakecloud-service.sh stop
```

## CI behavior

The `molecule` job in `.github/workflows/main.yml`:

1. Checks whether the matrix scenario is listed in `fakecloud_scenarios.txt`.
2. Starts fakecloud before `molecule test` when required.
3. Exports AWS client environment variables for that run only.
4. Stops fakecloud in an `always()` cleanup step.

Scenarios that only mock AWS or do not call AWS APIs do not need to be listed.

## Current fakecloud scenarios

| Scenario | What it tests |
| --- | --- |
| `integration_ec2_ami_copy` | `infra.ado.ec2_ami_copy` cross-region copy with `name=` set (rename) |
| `integration_ec2_ami_copy_keep_name` | `infra.ado.ec2_ami_copy` cross-region copy with `name` omitted (reuse source name) |

Add rows here when new scenarios opt in.
