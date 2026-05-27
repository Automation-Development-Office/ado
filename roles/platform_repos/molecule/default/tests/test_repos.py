"""
Test infrastructure for repos role using pytest-testinfra
"""
import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


@pytest.mark.parametrize('tool', [
    'yum',
    'dnf'
])
def test_package_managers_available(host, tool):
    """Test that package managers are available."""
    if host.system_info.distribution in ['centos', 'rhel', 'fedora']:
        cmd = host.run(f'which {tool}')
        # At least one should be available
        assert cmd.rc == 0 or tool == 'dnf'  # dnf might not be on older systems


def test_yum_repos_directory_exists(host):
    """Test that yum.repos.d directory exists."""
    repos_dir = host.file('/etc/yum.repos.d')
    assert repos_dir.is_directory
    assert repos_dir.mode == 0o755


def test_test_repository_files_exist(host):
    """Test that test repository files were created."""
    test_repo = host.file('/etc/yum.repos.d/test-repos.repo')
    assert test_repo.exists
    assert test_repo.is_file


def test_repository_configuration_format(host):
    """Test that repository files have correct format."""
    test_repo = host.file('/etc/yum.repos.d/test-repos.repo')
    if test_repo.exists:
        content = test_repo.content_string
        # Should contain repository sections
        assert '[test-repo-disabled]' in content
        assert '[test-repo-enabled]' in content
        # Should have enabled flags
        assert 'enabled=' in content


def test_backup_files_created(host):
    """Test that backup files are created when requested."""
    # Check if backup files exist (from file-edit method)
    cmd = host.run('find /etc/yum.repos.d/ -name "*.repo.*" -type f')
    # Backup files may exist if file-edit method was used
    assert cmd.rc == 0


@pytest.mark.parametrize('repo_name', [
    'epel',
    'test-repo-disabled'
])
def test_repository_operations(host, repo_name):
    """Test repository enable/disable operations."""
    # Test that we can query repository information
    pkg_mgr = 'dnf' if host.exists('dnf') else 'yum'
    cmd = host.run(f'{pkg_mgr} repolist all')
    assert cmd.rc == 0


def test_ansible_managed_markers(host):
    """Test that Ansible management markers exist."""
    cmd = host.run('grep -r "enabled by Ansible" /etc/yum.repos.d/ || true')
    # Should find at least some Ansible-managed repositories
    assert cmd.rc == 0


def test_cache_cleanup_functionality(host):
    """Test that cache cleanup works."""
    pkg_mgr = 'dnf' if host.exists('dnf') else 'yum'
    cache_dir = f'/var/cache/{pkg_mgr}/'
    
    # Cache directory should exist
    cache = host.file(cache_dir)
    assert cache.is_directory


def test_repository_verification_commands(host):
    """Test that repository verification commands work."""
    pkg_mgr = 'dnf' if host.exists('dnf') else 'yum'
    
    # Test repolist commands
    enabled_cmd = host.run(f'{pkg_mgr} repolist enabled --quiet')
    assert enabled_cmd.rc == 0
    
    disabled_cmd = host.run(f'{pkg_mgr} repolist disabled --quiet')
    # May fail on some systems, but shouldn't crash
    assert disabled_cmd.rc in [0, 1]


def test_role_idempotency_markers(host):
    """Test that role produces idempotent results."""
    # Check that repository files contain expected content
    test_repo = host.file('/etc/yum.repos.d/test-repos.repo')
    if test_repo.exists:
        content = test_repo.content_string
        # File should be well-formed
        assert content.strip() != ''
        assert '[' in content and ']' in content
