==================================
Infra Ado Collection Release Notes
==================================

.. contents:: Topics

v1.0.1
======

Minor Changes
-------------

- Add OpenShift Virtualization VM launch survey options for image preference, instance type, custom CPU and memory, disk size, static networking, password setup, and optional root SSH.
- Add Satellite install sizing, storage mount, deployment version, RHN organization, location, admin password, and activation key defaults to the bootstrap env var generator so UI and CLI preflight runs can populate the Satellite install role.
- Add default Satellite install tuning tiers and storage mount definitions to the Satellite install role.
- Add optional OpenShift Virtualization VM provisioning to bootstrap generation, including component vars, generated playbook repo content, and an AAP job template for CLI and UI preflight runs.
- Limit OpenShift Virtualization preflight-derived values to the OpenShift API endpoint, API token, TLS verification setting, and SSH public key so VM sizing and guest customization are controlled from the AAP launch survey.
- bootstrap_controller - Publishes the generated infra.ado collection to AAP Hub on AAP 2.5+ runs when the Hub publish option is enabled.
- bootstrap_controller - Stops after the AAP Hub publish step when the collection-only update flag is enabled.
- bootstrap_generate_env_vars - Added a collection-only Hub update flag so callers can update infra.ado in AAP Hub without generating component bootstrap content.
- bootstrap_generate_env_vars - Added a generated force-update toggle for publishing the bundled infra.ado collection to validated content in AAP Hub.
- collection - Fill out galaxy metadata with ADO project links, tags, and runtime collection dependencies.
- collection - Standardize the collection and role Ansible requirement metadata on ansible-core 2.16.
- roles - Flatten task entrypoints that only imported a single task file.

Bugfixes
--------

- Apply generated AAP inventory sources directly with ansible.controller so Satellite dynamic inventory sources are created when enabled from either the UI preflight JSON or CLI variables.
- Generated env var YAML now suppresses YAML anchors and preserves machine credential SSH private keys with a trailing newline instead of extra spaces.
- Keep Automation Hub and optional runtime collections out of galaxy.yml hard dependencies so installing the built infra.ado artifact does not fail when public Galaxy cannot resolve Red Hat or local-only collections.
- Normalize generated AAP survey choices so list values remain separate options instead of collapsing into a single dropdown entry.
- Remove remaining install-time galaxy.yml dependency resolution so pod and offline installs of infra.ado use container-provided collection tarballs.
- Satellite RHN organization IDs and activation keys are written as vault-backed values, with activation keys preserved when supplied by the UI.
- Satellite bootstrap playbooks now load generated env vars from the project root when running under AAP and enable become where host changes require it.
- Satellite install VG name is now generated from preflight/CLI input and raw installer-only fields are no longer duplicated under generic component config.
- Satellite install role defaults and task references now consistently use `satellite_install_rhn_*`, `satellite_install_size*`, `satellite_install_min_*`, and other non-duplicated install variable names.
- Satellite storage install variables now use the names consumed by the storage tasks, including `satellite_install_vg_name`, `satellite_install_req_dirs`, and `satellite_install_data_*`.
- Stop silently removing checked Satellite dynamic inventory sources during AAP credential-type preflight unless the compatibility skip flag is explicitly enabled.
- bootstrap_controller - Corrects AAP controller auth preflight messages to reference the generated aap_vault.yml file.
- bootstrap_controller - Loads generated AAP config variables and enables the AAP apply path for collection-only Hub update runs so the Hub publish step is not skipped.
- bootstrap_controller - Passes the generated AAP Hub repository target when publishing infra.ado so collection updates land in validated content instead of the published repository.
- bootstrap_controller - Stops waiting indefinitely on AAP Hub collection import processing after the upload is submitted so UI runs can return the final recap.
- bootstrap_generate_env_vars - Handles empty component and platform lists when running in AAP Hub collection-only update mode.
- bootstrap_generate_env_vars - Treats an empty Satellite deployment version as missing and writes the default 6.19 value.
- bootstrap_generate_env_vars - point the generated AAP execution environment at the supported AAP 2.6 RHEL 9 execution environment image instead of the generic AWX EE image so Satellite inventory syncs can load redhat.satellite.foreman.
- bootstrap_generate_env_vars - render the Satellite TLS validation setting into dynamic inventory source vars so AAP Satellite inventory syncs honor the UI and CLI skip TLS setting.
- bootstrap_generate_playbook_repo - Generates project collection requirements with an infra.ado version pin and AAP Hub source URL so AAP project syncs install the collection version containing newly generated roles such as ocp_virtualization.
- satellite_config - Defaults the Satellite deployment version to 6.19 for repository label generation.
- satellite_install - Defaults the Satellite deployment version to 6.19 so installs do not fail preliminary validation when generated vars omit the version.

v1.0.0
======

Minor Changes
-------------

- Add RHEL patching survey prompts for reboot behavior, package selection, package state, exclusions, disabled repositories, cache refresh, kernel cleanup, and skip-broken handling.
- Add Satellite service account inputs to generated environment vars so Satellite configuration can connect using UI or CLI-provided credentials.
- Add optional Satellite 6 dynamic inventory source generation for AAP, including a Satellite credential and inventory source settings for UI and CLI preflight runs.
- Added ACM bootstrap playbook and job template coverage so selected ACM components produce AAP content.
- Added OpenShift htpasswd, console banner, and cert-manager configuration variables for generated UI and CLI preflight runs.
- Added an OpenShift bootstrap workflow that includes selected admin htpasswd, cert-manager, console banner, RHBK, Grafana, GitLab, Pega, Kafka, AAP, ECK, GitOps, 389ds, OADP, Quay, ACS, and ACM job templates when those templates are generated.
- Bootstrap generation now removes playbook, environment variable, vault, and AAP job template artifacts for components that are no longer selected.
- Check AAP controller API connectivity before applying bootstrap controller objects and run a configurable demo job template smoke test.
- Correct the Satellite registration job template survey definition to use survey_spec and the standard bootstrap controller variables.
- Normalize RHEL patching list inputs so AAP survey text answers can be used as package, exclude, and disabled repository lists.
- Sync generated bootstrap playbook repositories with the remote branch before pushing so repeated UI or CLI generation runs can rebase on origin first.
- aap_build_ee - Added optional ``aap_build_ee_ansible_core`` and ``aap_build_ee_ansible_runner`` variables for minimal base image builds.
- aap_build_ee - Normalized ``aap_build_ee_collections`` input to support dict, list, and flat object formats when rendering ``requirements.yml``.
- aap_build_ee - Updated ``aap_build_ee_collections`` to accept a mapping of collection name to version constraint for generated ``requirements.yml``.
- ado-preflight-ui - Add Satellite field help, consistent skip-TLS wording, IDM configuration controls, immediate SSH key paste support, and an end-of-run ADO bootstrap recap.
- bootstrap_controller - add an AAP job template for RHEL STIG hardening with surveys for environment, compliance profile, and STIG profile.
- bootstrap_controller - attach the organization label to generated AAP job templates and workflow templates so each bootstrap run has an org-based top-level filter label in addition to component labels.
- bootstrap_controller - prefix generated job and workflow template names with the configured AAP organization.
- bootstrap_controller - verify the organization label exists in AAP after label creation so missing domain/filter labels fail visibly during bootstrap.
- bootstrap_generate_env_vars - Added generated AAP Machine credential support for RHEL, Satellite, and patching workflows, including ``vault_machine_cred.yml`` for SSH key material.
- bootstrap_generate_env_vars - Prefer component app selections over stale selected_component_apps values when importing older preflight JSON files.
- bootstrap_generate_env_vars - Preserve UI and CLI IDM configuration fields for DNS, replica, certificate, custom certificate, and auto-forwarder settings while removing the obsolete IDM storage value.
- bootstrap_generate_env_vars - add AAP additional credential inputs, org-based AAP object naming, and hub collection toggle vars for UI and CLI preflight flows.
- bootstrap_generate_env_vars - allow UI and CLI preflight JSON RHEL STIG options to generate the STIG component artifacts and profile vars.
- bootstrap_generate_env_vars - map OpenShift LDAP, OAuth/RHBK, route discovery, and pull secret checkboxes to distinct component app keys so UI and CLI payloads can select them independently.
- bootstrap_generate_playbook_repo - add a RHEL STIG hardening bootstrap playbook and optional generated repository STIG requirements for ``redhat.rhel_system_roles`` without making it a hard dependency of ``infra.ado`` installation.
- ci - Add changelog preview for dev pre-releases, including release notes and a downloadable ``CHANGELOG-preview.rst`` asset built from accumulated fragments.
- ci - Added ADO collection roles to ``mock_roles`` and excluded generated bootstrap seed payloads from source lint checks.
- ci - Added automatic collection build and GitHub Release asset attachment for dev tag pre-releases and published releases. Ansible Galaxy publish is now manual via the Release infra.ado workflow_dispatch job.
- ci - Generate ``CHANGELOG.rst`` from accumulated changelog fragments automatically when a GitHub Release is published, commit the result to ``main``, and include the changelog in the release collection tarball.
- docs - Add a role documentation index to the collection README with links to each role README.
- ocp_console_banner - accept add/update/delete state aliases while keeping present/new/absent compatibility.
- rhel_ext_system_roles - add support for invoking the upstream STIG RHEL system role through the existing wrapper.
- rhel_repos - Added Podman Molecule integration scenario on UBI 8 and UBI 9.
- satellite_config - Added a condition so third-party products and repositories are created on Satellite only when satellite_products is defined and non-empty.
- satellite_config - Added a condition to create third-party products and repositories on Satellite only when satellite_products is defined and non-empty.
- satellite_config - Added condition to create 3rd party products and repositories on Satellite only when satellite_products is defined and non-empty.

Breaking Changes / Porting Guide
--------------------------------

- rhel_repos - Renamed role from ``platform_repos``; use ``infra.ado.rhel_repos`` and ``rhel_repos_*`` variables instead of ``platform_repos_*``.

Removed Features (previously deprecated)
----------------------------------------

- platform_ec2 - Removed role.

Bugfixes
--------

- Add generated RHEL compliance and Satellite install/config/content-view playbooks and job templates, plus RHEL and Satellite workflow templates that target the matching generated component inventories.
- Attach the plain organization label to generated job templates and workflows so AAP domain/filter views can show the organization grouping.
- Create an organization label/domain such as ADO and keep generated job-template and workflow labels organization-prefixed.
- Generate both a focused patching workflow and a full RHEL workflow with simplified workflow nodes so AAP creates workflow templates reliably.
- Generate component-specific AAP inventories so the default inventory contains only localhost, RHEL managed hosts use the RHEL inventory, IDM hosts use the IDM inventory, and Satellite server jobs use the Satellite server inventory.
- Generate workflow template labels as top-level label lists instead of related label strings so infra.aap_configuration can create workflow templates without failing on missing label object names.
- Ignore stale component app selections from inactive groups so an OpenShift run with old RHEL/Satellite JSON state does not enable Satellite dynamic inventory or require Satellite service account fields.
- Keep optional OpenShift configuration jobs, such as Console Banner and Admin HTPasswd, as independent workflow start branches so they are added to AAP workflows even when other optional OpenShift jobs are not selected.
- Load OpenShift htpasswd and console banner jobs from vars_openshift and vault_openshift so selected OpenShift runs do not depend on ungenerated vars_htpasswd or vars_common files.
- Load generated AAP and component vault files before rendering controller config files so Satellite dynamic inventory credentials can reference generated vault variables.
- Map generated workflow config files to the controller_workflows dispatcher variable so AAP workflow templates are applied, not only written to Git.
- Normalize additional AAP credential names and Satellite dynamic inventory object names to the organization-prefixed naming pattern.
- Normalize generated AAP project names to the organization-prefixed naming pattern so UI and CLI inputs such as test-project become RH-test-project when the organization is RH.
- Normalize generated primary AAP Vault and Machine credential names to the organization-prefixed naming pattern so UI and CLI inputs such as test-vault and test-machine become RH-test-vault and RH-test-machine when the organization is RH.
- Normalize generated primary AAP inventory names to the organization-prefixed naming pattern so inputs such as test-inventory become RH-test-inventory when the organization is RH.
- Preflight the optional Satellite 6 dynamic inventory credential type before applying AAP credentials, and skip only the Satellite inventory source when that credential type is unavailable.
- Preserve vault variable references in generated controller credential config files instead of resolving secrets during config generation.
- Prune generated workflow nodes that reference unselected job templates so partial OpenShift app selections do not create invalid AAP workflows.
- Refresh generated AAP config and vault files on preflight JSON runs so UI reruns do not keep stale controller object definitions.
- Reload generated controller config files before applying AAP objects so split inventories, hosts, inventory sources, labels, job templates, and workflow templates are created from the current UI or CLI run.
- Render additional AAP credentials with credential-type-specific inputs, so Vault credentials use vault_password instead of machine credential fields.
- Render generated Console Banner survey choices as AAP-compatible newline-separated options so the default update action is accepted and OpenShift workflow creation is not blocked during AAP dispatch.
- Restore generated vault file encryption for preflight/UI runs and allow noninteractive CLI runs to provide a vault password file.
- Skip the post-AAP-config Git push when only AAP configs are generated and no playbook repository was generated.
- Stop adding the Satellite TLS verification flag to Satellite credential inputs because AAP credential schemas may not accept it as a credential field.
- Treat Satellite dynamic inventory as enabled when older preflight JSON selects Satellite but omits the dynamic inventory setting.
- aap_build_ee - Fixed ``ansible_core`` and ``ansible_runner`` rendering to use ansible-builder 3.x ``package_pip`` object schema.
- bootstrap_controller - Continue bootstrap runs when the optional smoke-test job template is missing after AAP connectivity succeeds.
- bootstrap_controller - Report safe AAP connectivity failure details instead of stopping on a fully censored no_log result, and persist the UI or CLI TLS validation setting into generated AAP vars.
- bootstrap_controller - Use the AAP 2.5 and 2.6 controller gateway API path for connectivity and smoke-test checks while keeping the AAP 2.4 controller API path.
- bootstrap_controller - include the UI or CLI supplied environment name in generated AAP job and workflow template survey choices and use it as the default environment.
- bootstrap_controller - include the console banner job template in generated OpenShift workflows and expose add/update/delete survey choices for banner management.
- bootstrap_controller - only generate optional OpenShift and RHBK AAP job templates when their matching options are selected, preventing unchecked resources from being created in AAP.
- bootstrap_generate_env_vars - gate OpenShift HTPasswd admin and console banner values behind `component_options.openshift` entries so UI and CLI preflight runs only generate those optional settings when selected.
- bootstrap_generate_env_vars - infer OpenShift console banner and HTPasswd option apps from submitted option values as a fallback for older UI payloads that omitted `component_options`.
- bootstrap_generate_env_vars - prefer modern `components` and `component_apps` preflight fields over the legacy `selected_component_apps` list so OpenShift option changes are not collapsed to a selected child app such as RHBK.
- bootstrap_generate_playbook_repo - Fixed generated bootstrap seed playbook YAML indentation and malformed ``vars_files`` entries so generated playbooks pass syntax and lint checks.
- bootstrap_generate_playbook_repo - Fixed generated bootstrap seed playbooks to reference real role names for ``include_role`` tasks.
- bootstrap_generate_playbook_repo - generate an OpenShift-scoped console banner playbook when the OpenShift console banner option is selected so UI and CLI runs create the workflow job target under `playbooks/openshift`.
- bootstrap_generate_playbook_repo - only copy optional OpenShift LDAP, OAuth/RHBK, route discovery, pull secret, and RHBK realm/client/IDP/ federation playbooks when their matching options are selected.
- ci - Ensure changelog fragments are only consumed and deleted when an official GitHub Release is published. Dev tag pushes and pre-releases now use preview-only changelog generation with a post-run verification that repository fragments are unchanged.
- ci - Fix changelog PR creation after releases by removing the generated-only guard, staging fragment deletions correctly, and improving PR branch handling.
- ci - Fix changelog generation to use ``antsibull-changelog release --version``, render ``CHANGELOG.rst`` from fragments, and set GitHub Release notes from the compiled changelog instead of auto-generated commit summaries.
- ci - Install mikefarah/yq in collection build jobs instead of the Ubuntu ``yq`` package, which does not support ``yq -i`` for updating ``galaxy.yml`` version on tag builds.
- ci - Move Ansible Galaxy publish to a separate manual-only workflow so GitHub Release events no longer trigger automatic Galaxy publication from ``main``.
- ci - Remove the non-compliant shebang from ``scripts/validate_release_version.py`` so ansible-test sanity shebang checks pass.
- ci - Stop overwriting ``galaxy.yml`` namespace during tag builds so release tarballs are built as ``infra.ado`` instead of ``ado.ado``.
- ci - Stop syncing ``.github/actions`` from ``main`` during release jobs so tag builds use the pipeline from the checked-out branch or tag ref.
- ci - Sync ``.github/actions`` from ``main`` during release jobs so tags use the current changelog tooling, validate release versions for antsibull-changelog compatibility, and fail early on invalid tags such as ``249.0.0.1-rc1``.
- ci - Use fully qualified ``refs/heads/`` refspec when pushing changelog release branches from detached HEAD checkouts in Actions.
- ocp_operatorgroups - Fixed task imports to reference existing ``create_operatorgroup.yml`` and ``delete_operatorgroup.yml`` task files.

Documentation Changes
---------------------

- Align bootstrap playbook examples with role README basic usage examples.
- CODE_OF_CONDUCT - Added repository Code of Conduct with Ansible Community CoC adoption and ADO addendum.
- bootstrap_resolve_component - Replaced a smart quote in the role README so Ansible sanity ``no-smart-quotes`` passes.
- ci - Expanded ``.github/README.md`` into a full developer and maintainer guide covering all GitHub Actions workflows, PR requirements, Molecule testing, local validation, collection builds, dev pre-releases, official releases, and troubleshooting.
- kafka_install - Restored the README environment authentication section required by the role's Molecule verify scenario.
- roles - Normalized role README files to match the repository role README format template and replaced generated placeholder text with role-specific summaries, variables, usage, and test notes.
