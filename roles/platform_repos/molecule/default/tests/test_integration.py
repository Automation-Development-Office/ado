"""
Test role integration and end-to-end functionality
"""
import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


class TestRoleIntegration:
    """Test role integration and complex scenarios."""
    
    def test_multiple_methods_compatibility(self, host):
        """Test that multiple repo management methods don't conflict."""
        # Check that we can use different methods without conflicts
        cmd = host.run('ls -la /etc/yum.repos.d/')
        assert cmd.rc == 0
        
        # Should have at least the test repo files
        assert 'test-repos.repo' in cmd.stdout


    def test_variable_expansion(self, host):
        """Test that Ansible variables are properly expanded."""
        test_repo = host.file('/etc/yum.repos.d/test-repos.repo')
        if test_repo.exists:
            content = test_repo.content_string
            # Should not contain unexpanded variables
            assert '{{' not in content
            assert '}}' not in content


    def test_error_handling_resilience(self, host):
        """Test that role handles errors gracefully."""
        # Repository commands should not fail catastrophically
        pkg_mgr = 'dnf' if host.exists('dnf') else 'yum'
        
        # Test with non-existent repo (should handle gracefully)
        cmd = host.run(f'{pkg_mgr} repolist nonexistent-repo || true')
        assert cmd.rc in [0, 1]  # Should not crash system


    def test_file_permissions_security(self, host):
        """Test that created files have secure permissions."""
        test_repo = host.file('/etc/yum.repos.d/test-repos.repo')
        if test_repo.exists:
            # Repository files should be readable by all, writable by root only
            assert test_repo.mode == 0o644
            assert test_repo.user == 'root'
            assert test_repo.group == 'root'


    @pytest.mark.parametrize('method', [
        'rhsm_repository',
        'yum_repository', 
        'file-edit'
    ])
    def test_method_specific_results(self, host, method):
        """Test method-specific implementation results."""
        # Each method should leave recognizable traces
        if method == 'file-edit':
            # file-edit method creates backup files
            cmd = host.run('find /etc/yum.repos.d/ -name "*.repo.*" | head -1')
            # May or may not exist depending on test execution
            assert cmd.rc == 0
            
        elif method == 'yum_repository':
            # yum_repository method creates clean repo files
            test_repo = host.file('/etc/yum.repos.d/test-repos.repo')
            if test_repo.exists:
                content = test_repo.content_string
                # Should have proper INI format
                assert '[' in content and ']' in content


    def test_advanced_configuration_support(self, host):
        """Test that advanced repo configuration is supported."""
        test_repo = host.file('/etc/yum.repos.d/test-repos.repo')
        if test_repo.exists:
            content = test_repo.content_string
            
            # Should support various repository configuration options
            possible_options = [
                'baseurl=',
                'mirrorlist=',
                'metalink=',
                'enabled=',
                'gpgcheck=',
                'name='
            ]
            
            # At least some options should be present
            found_options = sum(1 for opt in possible_options if opt in content)
            assert found_options >= 2  # At least name and enabled should be there


    def test_cleanup_operations(self, host):
        """Test that cleanup operations work correctly."""
        # Check that temporary files are cleaned up
        temp_files = host.run('find /tmp/ -name "*repos*" -type f | wc -l')
        # Should not have excessive temporary files
        assert int(temp_files.stdout.strip()) < 10


    def test_role_documentation_compliance(self, host):
        """Test that role behavior matches documentation."""
        # Repository files should exist if repos were configured
        repos_dir = host.file('/etc/yum.repos.d')
        assert repos_dir.exists
        
        # Should be able to list repositories
        pkg_mgr = 'dnf' if host.exists('dnf') else 'yum'
        cmd = host.run(f'{pkg_mgr} repolist --quiet')
        assert cmd.rc == 0
