"""
Conftest for RHSM-specific pytest configuration and fixtures
"""
import pytest


@pytest.fixture(scope='session')
def rhsm_available(host):
    """Check if RHSM is available and functional."""
    cmd = host.run('which subscription-manager')
    return cmd.rc == 0


@pytest.fixture(scope='session')
def is_registered_to_rhsm(host):
    """Check if system is registered to RHSM."""
    if not host.exists('subscription-manager'):
        return False
    
    cmd = host.run('subscription-manager status')
    return cmd.rc == 0


@pytest.fixture(scope='session')
def rhsm_config_dir():
    """RHSM configuration directory."""
    return '/etc/rhsm'


@pytest.fixture(scope='session')
def rhsm_cert_dir():
    """RHSM certificate directory."""
    return '/etc/pki/entitlement'


@pytest.fixture
def skip_if_no_rhsm(host):
    """Skip test if RHSM is not available."""
    if not host.exists('subscription-manager'):
        pytest.skip("subscription-manager not available")


@pytest.fixture
def mock_rhsm_repos():
    """Mock RHSM repository data for testing."""
    return [
        {
            'repo_id': 'rhel-8-for-x86_64-baseos-rpms',
            'repo_name': 'Red Hat Enterprise Linux 8 for x86_64 - BaseOS (RPMs)',
            'enabled': True
        },
        {
            'repo_id': 'rhel-8-for-x86_64-appstream-rpms', 
            'repo_name': 'Red Hat Enterprise Linux 8 for x86_64 - AppStream (RPMs)',
            'enabled': False
        }
    ]


def pytest_configure(config):
    """Configure pytest with RHSM-specific markers."""
    config.addinivalue_line(
        "markers", "requires_registration: mark test as requiring RHSM registration"
    )
    config.addinivalue_line(
        "markers", "subscription_manager: mark test as requiring subscription-manager"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection for RHSM-specific tests."""
    for item in items:
        # Add subscription_manager marker to all tests in this scenario
        item.add_marker(pytest.mark.subscription_manager)
        
        # Add requires_registration marker to tests that need registration
        if any(keyword in item.name.lower() for keyword in ['register', 'subscription', 'entitle']):
            item.add_marker(pytest.mark.requires_registration)
