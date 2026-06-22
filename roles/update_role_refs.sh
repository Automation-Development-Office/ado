#!/bin/bash

sed -i \
-e 's/openshift_configure_devspaces_user_config/ocp_devspaces_user_config/g' \
-e 's/openshift_configure_efs_csi_driver/ocp_efs_csi/g' \
-e 's/openshift_configure_iscsi_storage/ocp_iscsi_storage/g' \
-e 's/openshift_configure_kube_descheduler/ocp_descheduler/g' \
-e 's/openshift_configure_ldap_auth/ocp_ldap_auth/g' \
-e 's/openshift_configure_logging/ocp_logging/g' \
-e 's/openshift_configure_nfs_storage/ocp_nfs_storage/g' \
-e 's/openshift_configure_oidc_auth/ocp_oidc_auth/g' \
-e 's/openshift_data_foundation/ocp_data_foundation/g' \
-e 's/openshift_install_aap24/ocp_aap24/g' \
-e 's/openshift_install_aap25/ocp_aap25/g' \
-e 's/openshift_install_aap26/ocp_aap26/g' \
-e 's/openshift_install_acm/ocp_acm/g' \
-e 's/openshift_install_acs/ocp_acs/g' \
-e 's/openshift_install_cert_manager/ocp_cert_manager/g' \
-e 's/openshift_install_devspaces/ocp_devspaces/g' \
-e 's/openshift_install_dirsrv/ocp_dirsrv/g' \
-e 's/openshift_install_elastic_eck/ocp_elastic_eck/g' \
-e 's/openshift_install_gitlab_runner/ocp_gitlab_runner/g' \
-e 's/openshift_install_gitops/ocp_gitops/g' \
-e 's/openshift_install_grafana/ocp_grafana/g' \
-e 's/openshift_install_loki_stack/ocp_loki/g' \
-e 's/openshift_install_oadp/ocp_oadp/g' \
-e 's/openshift_install_ocp_virt/ocp_virtualization/g' \
-e 's/openshift_install_postfix/ocp_postfix/g' \
-e 's/openshift_install_quay/ocp_quay/g' \
-e 's/openshift_install_rhbk/ocp_rhbk/g' \
-e 's/openshift_tools_create_htpass_admin_user/ocp_htpasswd_admin/g' \
-e 's/openshift_tools_create_service_accounts/ocp_service_accounts/g' \
-e 's/openshift_tools_discover_routes/ocp_discover_routes/g' \
-e 's/openshift_tools_ensure_alt_routes_from_list/ocp_alt_routes/g' \
-e 's/openshift_tools_ensure_component_route/ocp_component_route/g' \
-e 's/openshift_tools_get_routes/ocp_routes/g' \
-e 's/openshift_tools_lookup_operator_defaults/ocp_operator_defaults/g' \
-e 's/openshift_tools_manage_operator_groups/ocp_operator_groups/g' \
-e 's/openshift_tools_print_crd/ocp_print_crd/g' \
-e 's/openshift_tools_rhbk_get_client_secrets/ocp_rhbk_client_secrets/g' \
-e 's/openshift_tools_search_dirsrv/ocp_search_dirsrv/g' \
-e 's/openshift_tools_secret_replicator/ocp_secret_replicator/g' \
-e 's/openshift_tools_subscription_operator/ocp_operator_subscription/g' \
-e 's/openshift_tools_update_pull_secrets/ocp_pull_secrets/g' \
-e 's/openshift_tools_wait_for_operator_ready/ocp_wait_operator/g' \
-e 's/openshift_tools_wait_for_pods_running/ocp_wait_pods/g' \
$(find . -type f \( -name "*.yml" -o -name "*.yaml" -o -name "*.md" -o -name "*.j2" -o -name "*.py" \))

