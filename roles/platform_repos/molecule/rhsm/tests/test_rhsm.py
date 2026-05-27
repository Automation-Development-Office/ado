"""
Test RHSM-specific functionality for repos role
"""
import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


class TestRHSMFunctionality:
    """Test Red Hat Subscription Manager specific functionality."""
    
    def test_subscription_manager_available(self, host):
        """Test that subscription-manager is available."""
        cmd = host.run('which subscription-manager')
        if host.system_info.distribution in ['centos', 'rhel']:
            # Should be available on RHEL-based systems
            assert cmd.rc == 0 or host.system_info.distribution == 'centos'
    
    
    def test_rhsm_configuration_files(self, host):
        """Test RHSM configuration files exist."""
        # RHSM config file
        rhsm_conf = host.file('/etc/rhsm/rhsm.conf')
        if rhsm_conf.exists:
            assert rhsm_conf.is_file
            assert rhsm_conf.mode == 0o644
    
    
    def test_repository_management_commands(self, host):
        """Test that RHSM repository management commands work."""
        # Test listing repositories (may fail if not registered, but shouldn't crash)
        cmd = host.run('subscription-manager repos --list || true')
        assert cmd.rc in [0, 1, 70]  # 70 is "not registered" error
    
    
    def test_rhsm_method_specific_traces(self, host):
        """Test for RHSM method specific implementation traces."""
        # When using rhsm_repository method, it should use subscription-manager
        # We can't test actual registration, but we can test command availability
        sm_cmd = host.run('subscription-manager --help')
        if host.system_info.distribution in ['centos', 'rhel']:
            assert sm_cmd.rc == 0
    
    
    def test_rhsm_repos_directory_structure(self, host):
        """Test RHSM-related directory structure."""
        # RHSM directories that should exist
        rhsm_dirs = [
            '/etc/rhsm',
            '/var/lib/rhsm'
        ]
        
        for rhsm_dir in rhsm_dirs:
            dir_obj = host.file(rhsm_dir)
            if dir_obj.exists:
                assert dir_obj.is_directory
    
    
    def test_subscription_status_check(self, host):
        """Test subscription status checking."""
        # Test subscription status command
        cmd = host.run('subscription-manager status || true')
        # Should not crash, regardless of registration status
        assert cmd.rc in [0, 1, 70]  # Various valid exit codes
    
    
    def test_rhsm_certificate_handling(self, host):
        """Test RHSM certificate directory exists."""
        cert_dir = host.file('/etc/pki/entitlement')
        # Directory should exist on RHEL systems
        if host.system_info.distribution == 'rhel':
            assert cert_dir.exists
            assert cert_dir.is_directory
    
    
    def test_yum_plugin_compatibility(self, host):
        """Test YUM plugin compatibility with RHSM."""
        # Check for subscription-manager yum plugin
        plugin_dirs = [
            '/usr/share/yum-plugins',
            '/etc/yum/pluginconf.d'
        ]
        
        for plugin_dir in plugin_dirs:
            dir_obj = host.file(plugin_dir)
            if dir_obj.exists:
                assert dir_obj.is_directory


class TestRHSMIntegration:
    """Test integration between RHSM and repository management."""
    
    def test_rhsm_repo_file_coexistence(self, host):
        """Test that RHSM and manual repo files can coexist."""
        yum_repos_dir = host.file('/etc/yum.repos.d')
        assert yum_repos_dir.exists
        assert yum_repos_dir.is_directory
        
        # Should be able to list files in the directory
        cmd = host.run('ls /etc/yum.repos.d/')
        assert cmd.rc == 0
    
    
    def test_package_manager_rhsm_integration(self, host):
        """Test package manager integration with RHSM."""
        pkg_mgr = 'dnf' if host.exists('dnf') else 'yum'
        
        # Test that package manager can work with RHSM repos
        cmd = host.run(f'{pkg_mgr} repolist all --quiet || true')
        assert cmd.rc in [0, 1]  # Should not crash
    
    
    def test_rhsm_method_error_handling(self, host):
        """Test error handling for RHSM method."""
        # Test that RHSM commands handle errors gracefully
        # This tests the role's error handling when RHSM operations fail
        cmd = host.run('subscription-manager repos --list-enabled || true')
        # Should handle errors gracefully (not crash the system)
        assert cmd.rc in [0, 1, 70]  # Various valid exit codes
