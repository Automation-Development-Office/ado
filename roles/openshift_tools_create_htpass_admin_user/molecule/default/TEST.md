# TEST — create_htpass_admin_user (Molecule)

## Goals
- Prove the role adds an HTPasswd IdP **non-destructively**.
- Verify Secret exists and includes the user.
- (Optional) Verify `cluster-admin` CRB.
- Prove delete removes only this IdP + Secret + (optional) CRBs.

## Running
```bash
export K8S_AUTH_HOST="https://api.<cluster>:6443"
export K8S_AUTH_API_KEY="<token>"
export K8S_AUTH_VERIFY_SSL="no"

molecule converge
molecule idempotence
molecule destroy
```

## Checks

### Converge
```bash
# IdP summary
oc get oauth cluster -o jsonpath='{range .spec.identityProviders[*]}{.name}{"\t"}{.type}{"\t"}{.mappingMethod}{"\t"}{.htpasswd.fileData.name}{"\n"}{end}'

# Secret has the user
oc -n openshift-config get secret htpasswd-admin-secret -o jsonpath='{.data.htpasswd}' | base64 -d | grep '^admin:'

# Operator health
oc get co authentication -o jsonpath='{.status.conditions[?(@.type=="Progressing")].status} {" "}{.status.conditions[?(@.type=="Degraded")].status} {" "}{.status.conditions[?(@.type=="Available")].status}{"\n"}'
```

### Idempotence
```bash
molecule idempotence
```

### Destroy
```bash
# IdP gone
oc get oauth cluster -o jsonpath='{range .spec.identityProviders[*]}{.name}{"\n"}{end}' | grep -w htpasswd-admin || echo "gone"
# Secret gone
oc -n openshift-config get secret htpasswd-admin-secret || echo "gone"
# CRB gone (if created)
oc get clusterrolebinding cluster-admin-admin || echo "gone"
```