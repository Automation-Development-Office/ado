# Vendored upstream role

- Source: `infra.aap_utilities.aap_ocp_install`
- Collection version: `3.5.0`
- Repository: <https://github.com/redhat-cop/aap_utilities>
- Role source: <https://github.com/redhat-cop/aap_utilities/tree/devel/roles/aap_ocp_install>
- License: GPL-3.0-or-later

The implementation is vendored so generated ADO projects can install AAP on
OpenShift without downloading `infra.aap_utilities` during Controller project
sync. Local ADO behavior belongs in the wrapper role
`infra.ado.aap_ocp_install`; keep this directory aligned with upstream.
