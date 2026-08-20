# Grafana dashboard templates

Copied into generated playbook repos by `infra.ado.bootstrap_generate_playbook_repo`.

Layout matches Grafana multi-folder upload (`grafana_folders`):

| Grafana folder | Path | Mode |
|----------------|------|------|
| OpenshiftProd | `templates/Openshift/dashboards/*.json.j2` | Pinned to **Openshift-Prod** |
| OpenshiftDev | same templates | Pinned to **Openshift-Dev** |
| Openshift | same templates | **K8S** dropdown (Prod/Dev) — optional |
| RHACS | `templates/RHACS/dashboards/*.json` | As-is |

One template tree under `templates/Openshift/dashboards/` is uploaded multiple times.
`infra.ado.grafana_upload_dashboards` adapts UID/title/datasource per folder via
`datasource_mode: pin|multi|none`.

### Shared Openshift folder (K8S dropdown)

Controlled by `grafana_group_cluster_dashboards` (default **true**) and the preflight
Grafana checkbox **Also deploy shared Openshift folder with K8S Prod/Dev dropdown**.

When enabled, each dashboard in the **Openshift** folder has a **K8S** variable to
switch `Openshift-Prod` / `Openshift-Dev` (same pattern as cert-manager expiry).

### Datasources (ADO)

`infra.ado.grafana_create_datasource` creates:

| Datasource | Default source |
|------------|----------------|
| `Openshift-Prod` | Local `thanos-querier` (platform + user-workload) |
| `Openshift-Dev` | Remote Dev thanos-querier URL + `grafana-openshift-dev-prometheus` Secret |

### OpenShift template inventory

| File | Base UID |
|------|----------|
| `openshift-k8s-dashboard.json.j2` | `ado-ocp-k8s-dashboard` |
| `openshift-cluster-resource-overview.json.j2` | `ado-ocp-resource-overview` |
| `cert-manager-expiry.json.j2` | `ado-cert-manager-expiry` |
| `keycloak-metrics.json.j2` | `ado-keycloak-metrics` |
| `Openshift-Cluster-Overview.json.j2` | `ado-openshift-cluster-overview-json` |
| `openshift-api-monitoring.json.j2` | `k8s_system_apisrv` |
| `openshift-cluster-details.json.j2` | `icjpCppik` |
| `openshift-cluster-metrics.json.j2` | `dxkdT-eWz` |
| `openshift-node-full-border.json.j2` | `rYdddlPWk` |
| `openshift-pod-cluster-montitoring.json.j2` | `AAOMjeHmk` |
| `openshift-projects.json.j2` | `000000011` |
| `openshift-user-metrics.json.j2` | `isFoa0z7k` |
| `openshift_cluster_health.json.j2` | `bekvxj0fqfi80a` |

Pinned folders append `-prod` / `-dev` to the UID so Grafana can keep all three copies.

### RHACS

`rhacs-vulnerability-overview.json` (UID `ado-rhacs-vuln-posture`) uploads into the
**RHACS** folder.

Run **ADO | Deploy Grafana** (full) or **ADO | Deploy Grafana Dashboards**
(datasources + folders + import).

Example `grafana_folders` (defaults in `components_defaults.yml`):

```yaml
grafana_group_cluster_dashboards: true
grafana_folders:
  - name: OpenshiftProd
    source_type: path
    source: templates/Openshift
    dashboards_path: dashboards
    datasource_mode: pin
    datasource: Openshift-Prod
    uid_suffix: "-prod"
    title_cluster: Prod
  - name: OpenshiftDev
    source_type: path
    source: templates/Openshift
    dashboards_path: dashboards
    datasource_mode: pin
    datasource: Openshift-Dev
    uid_suffix: "-dev"
    title_cluster: Dev
  - name: Openshift
    source_type: path
    source: templates/Openshift
    dashboards_path: dashboards
    datasource_mode: multi
  - name: RHACS
    source_type: path
    source: templates/RHACS
    dashboards_path: dashboards
    datasource_mode: none
```
