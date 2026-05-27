"""
Conftest for pytest configuration and fixtures
"""
import pytest


@pytest.fixture(scope='session')
def ansible_facts(host):
    """Collect ansible facts for the host."""
    return host.ansible.get_variables()


@pytest.fixture(scope='session')
def package_manager(host):
    """Determine the package manager for the host."""
    if host.exists('dnf'):
        return 'dnf'
    elif host.exists('yum'):
        return 'yum'
    else:
        return None


@pytest.fixture(scope='session')
def is_rhel_based(host):
    """Check if the host is RHEL-based."""
    return host.system_info.distribution in ['centos', 'rhel', 'fedora']


@pytest.fixture(scope='session')
def repo_files_dir():
    """Repository files directory."""
    return '/etc/yum.repos.d'


@pytest.fixture
def test_repo_content():
    """Sample repository content for testing."""
    return """[test-repo-enabled]
name=Test Repository (Enabled)
baseurl=http://example.com/repo/enabled
enabled=1
gpgcheck=1

[test-repo-disabled]
name=Test Repository (Disabled)
baseurl=http://example.com/repo/disabled
enabled=0
gpgcheck=1
"""


@pytest.fixture
def cleanup_test_files(host):
    """Cleanup test files after tests."""
    yield
    # Cleanup any test files that might have been created
    host.run('rm -f /etc/yum.repos.d/test-*.repo')
    host.run('rm -f /etc/yum.repos.d/*.repo.*')  # Backup files


@pytest.fixture(scope='module')
def subscription_manager_available(host):
    """Check if subscription-manager is available."""
    cmd = host.run('which subscription-manager')
    return cmd.rc == 0


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "rhsm: mark test as requiring RHSM functionality"
    )
    config.addinivalue_line(
        "markers", "requires_internet: mark test as requiring internet access"
    )
    config.addinivalue_line(
        "markers", "destructive: mark test as potentially destructive"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add rhsm marker to RHSM-related tests
        if 'rhsm' in item.name.lower() or 'subscription' in item.name.lower():
            item.add_marker(pytest.mark.rhsm)
        
        # Add destructive marker to tests that modify system
        if any(keyword in item.name.lower() for keyword in ['cleanup', 'modify', 'delete']):
            item.add_marker(pytest.mark.destructive)
