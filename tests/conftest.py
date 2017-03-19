import pytest

import _socket_toggle


def pytest_runtest_setup():
    """ disable the internet. test-cases can explicitly re-enable """
    _socket_toggle.disable_socket()


@pytest.fixture(scope='function')
def enable_socket(request):
    """ re-enable socket.socket for duration of this test function """
    _socket_toggle.enable_socket()
    request.addfinalizer(_socket_toggle.disable_socket)
