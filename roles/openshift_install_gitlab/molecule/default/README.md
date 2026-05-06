OpenShift Token Setup & Running Molecule (READM.txt)
=====================================================

This guide shows how to:
1) Create a service account and long‑lived API token in OpenShift
2) Grant it cluster‑admin for testing
3) Run Molecule against your roles using that token

⚠️ SECURITY NOTE
----------------
Granting **cluster-admin** is powerful. Use only in lab/test environments.
For production, scope a narrower ClusterRole & RoleBinding to only the resources your role needs.


1) Prerequisites
----------------
- OpenShift CLI (`oc`) installed and logged in as a cluster-admin user
- Python 3.10+ and pip
- Ansible and Molecule
- Required collections and Python libs

Install helpful tools (adjust as needed):
    python3 -m pip install --user ansible-core molecule molecule-plugins[docker] kubernetes
    ansible-galaxy collection install kubernetes.core

(If you lint Markdown or Ansible, also consider: ansible-lint, markdownlint, etc.)


2) Create namespace, service account, and permissions
-----------------------------------------------------
Use the example namespace: **openshift-ansible**
(Namespaces prefixed with 'openshift-' are protected. You need cluster-admin to create it.)

Create namespace (ok if it already exists):
    oc new-project openshift-ansible || true
    # or: oc create namespace openshift-ansible || true

Create the service account:
    oc create sa ansible-sa -n openshift-ansible || true

Grant cluster-admin to the service account (two equivalent ways; pick one):

    # (A) Using 'oc adm policy' (recommended)
    oc adm policy add-cluster-role-to-user cluster-admin \
      -z ansible-sa -n openshift-ansible

    # (B) Using an explicit ClusterRoleBinding
    oc create clusterrolebinding ansible-sa-admin \
      --clusterrole=cluster-admin \
      --serviceaccount=openshift-ansible:ansible-sa \
      || true

Verify access (optional):
    oc auth can-i get namespaces \
      --as=system:serviceaccount:openshift-ansible:ansible-sa


3) Obtain a long-lived token
----------------------------
OpenShift 4.11+:
    export TOKEN="$(oc create token ansible-sa -n openshift-ansible --duration=876000h)"
    echo "$TOKEN"   # will look like: sha256~…

Older OpenShift (fallback if 'oc create token' not available):
    SA_SECRET="$(oc -n openshift-ansible get sa ansible-sa -o jsonpath='{.secrets[0].name}')"
    export TOKEN="$(oc -n openshift-ansible get secret "$SA_SECRET" -o jsonpath='{.data.token}' | base64 -d)"
    echo "$TOKEN"


4) Choose one authentication method for Molecule
------------------------------------------------

Option A — Environment variables (no kubeconfig needed)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Set the API server URL and token:
    export K8S_AUTH_HOST="https://api.<cluster-domain>:6443"
    export K8S_AUTH_API_KEY="$TOKEN"

TLS options (pick ONE):
    # Quick/untrusted lab cluster (self-signed):
    export K8S_AUTH_VERIFY_SSL=false

    # Preferred: verify SSL with a CA file
    export K8S_AUTH_VERIFY_SSL=true
    # Extract cluster CA from your kubeconfig (context #0 as a simple default):
    oc config view --raw -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d > ca.crt
    export K8S_AUTH_SSL_CA_CERT="$PWD/ca.crt"

Option B — Use kubeconfig instead of env vars
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Login as any user that can reach the cluster:
    oc login https://api.<cluster-domain>:6443 --username <user> --password <pass>
    # or use an SSO/login method appropriate for your environment

Then point Ansible at your kubeconfig (default is ~/.kube/config):
    export KUBECONFIG=~/.kube/config


5) Wire variables into Molecule (per-scenario example)
------------------------------------------------------
In your role’s scenario file: roles/<role>/molecule/default/molecule.yml

Add environment passthrough for the Ansible provisioner:
    provisioner:
      name: ansible
      env:
        # Use env‑var auth (Option A)
        K8S_AUTH_HOST: "${K8S_AUTH_HOST}"
        K8S_AUTH_API_KEY: "${K8S_AUTH_API_KEY}"
        K8S_AUTH_VERIFY_SSL: "${K8S_AUTH_VERIFY_SSL:-true}"
        K8S_AUTH_SSL_CA_CERT: "${K8S_AUTH_SSL_CA_CERT:-}"
        # Locate adjacent roles when testing inside a collection
        ANSIBLE_ROLES_PATH: "${MOLECULE_PROJECT_DIRECTORY}/.."

If you use the docker driver and rely on KUBECONFIG (Option B), mount it:
    platforms:
      - name: instance
        image: registry.access.redhat.com/ubi9/ubi
        volumes:
          - "${KUBECONFIG:-$HOME/.kube/config}:/root/.kube/config:ro"


6) Run Molecule
---------------
From the role directory (e.g., openshift/roles/<your role>):

Full test sequence:
    molecule test

Or individual steps:
    molecule converge
    molecule idempotence
    molecule verify
    molecule destroy

Tip: if your verify tasks call the API and your lab uses self‑signed certs,
either provide the CA file (preferred) or set K8S_AUTH_VERIFY_SSL=false.


7) Troubleshooting
------------------
- SSL self-signed errors:
    Use a real CA bundle: export K8S_AUTH_SSL_CA_CERT=/path/to/ca.crt
    or temporarily: export K8S_AUTH_VERIFY_SSL=false

- 403/Forbidden using the token:
    Ensure the ClusterRoleBinding exists and references the correct SA:
      oc get clusterrolebinding ansible-sa-admin -o yaml
    Re-verify access:
      oc auth can-i get namespaces --as=system:serviceaccount:openshift-ansible:ansible-sa

- 401/Unauthorized:
    Token missing/expired/typo. Recreate the token and re-export K8S_AUTH_API_KEY.

- Connection errors:
    Confirm K8S_AUTH_HOST is correct and reachable (https://api.<cluster-domain>:6443).

- Molecule can’t find your role:
    Set ANSIBLE_ROLES_PATH to the parent of the role (often ${MOLECULE_PROJECT_DIRECTORY}/..).


Appendix — Minimal verify task example (README check)
-----------------------------------------------------
Add to your scenario’s verify.yml to assert a role README exists:
    - name: Check README.md exists
      ansible.builtin.stat:
        path: "{{ lookup('env','MOLECULE_PROJECT_DIRECTORY') }}/README.md"
      register: readme_file

    - name: Fail if missing
      ansible.builtin.fail:
        msg: "README.md required for this role."
      when: not readme_file.stat.exists


