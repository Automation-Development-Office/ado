# Role: ado.openshift.wait_for_pods_running — Molecule

This scenario validates that the **wait_for_pods_running** role waits until matching Pods are **Running**/**Ready**.

- Fixture namespace: `test-wait-pods-molecule`
- Fixture deployment: `hello` (`replicas=2`, label `app=hello`)
- The role is invoked in **converge**; **verify** double-checks with `k8s_info` and runs README checks.

---

## Prerequisites

- Reachable OpenShift cluster (`oc` installed)
- Python 3.10+, `ansible-core`, `molecule`, `kubernetes` Python lib
- `kubernetes.core` collection

Install (example):
```bash
python3 -m pip install --user "ansible-core==2.19.1" "ansible-lint==24.7.1" molecule molecule-plugins kubernetes
ansible-galaxy collection install kubernetes.core
```

---

## Auth / TLS

Use kubeconfig or env vars:

```bash
# host + token
export K8S_AUTH_HOST="https://api.<cluster-domain>:6443"
export K8S_AUTH_API_KEY="$(oc -n openshift-ansible create token ansible-sa --duration=876000h)"
export K8S_AUTH_VERIFY_SSL=false  # or true with a CA: export K8S_AUTH_SSL_CA_CERT=/path/to/ca.crt

# or kubeconfig
export KUBECONFIG=~/.kube/config
```

---

## How to run

```bash
molecule test                # runs the full sequence
molecule converge            # create namespace, deploy fixture, run wait role
molecule idempotence
molecule verify              # assert pods/README
molecule destroy             # cleanup
```

---

## Scenario variables (defaults used in the plays)

- `name_space`: `test-wait-pods-molecule`
- `app_name`: `hello`
- `replicas`: `2`
- `validate_certs`: `false` (set true if you provide a CA)

---

## What the scenario does

1. **dependency** — install collections
2. **lint** — run `ansible-lint`
3. **syntax** — syntax check playbooks
4. **create** — (localhost driver setup)
5. **converge**
   - Use `ado.openshift.namespace` to create the test namespace
   - Create a small Deployment (pause image, 2 replicas, label `app=hello`)
   - **Run** `ado.openshift.wait_for_pods_running` to wait for pods Ready
6. **idempotence** — re-run converge, expect `changed=0`
7. **verify** — confirm pod count/Ready via `k8s_info`; README checks
8. **destroy** — delete namespace via the namespace role

> If your verify runs **after destroy** in your environment, move verify before destroy or limit verify to non-live checks.