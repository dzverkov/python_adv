import pytest

from actions import get_server_actions


@pytest.fixture
def expected_actions():
    return ['echo', 'send']


def test_expected_server_actions(expected_actions):
    server_actions = get_server_actions()
    for server_action in server_actions:
        assert server_action.get('action') in expected_actions
