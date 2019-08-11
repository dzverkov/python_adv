import pytest

from actions import resolve
from echo import controllers as echo_controllers
from messenger import controllers as messenger_controllers



@pytest.fixture
def expected_resolves():
    return [
        {'action': 'echo', 'controller': echo_controllers.get_echo},
        {'action': 'send', 'controller': messenger_controllers.send_message}
    ]


def test_expected_server_resolve(expected_resolves):
    for expected_resolve in expected_resolves:
        assert expected_resolve.get('controller') == resolve(expected_resolve.get('action'))
