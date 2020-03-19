import logging as log

import pytest

from pyjapi import JAPIClient


@pytest.fixture
def client():
    try:
        client = JAPIClient()
    except Exception:
        pytest.xfail("No backend available!")
    yield client


@pytest.mark.parametrize('cmd', [
    'japi_pushsrv_list',
    'japi_pushsrv_subscribe',
    'japi_pushsrv_unsubscribe',
])
def test_pushsrv_commands(client, cmd):
    r = client.query(cmd)
    log.info(r)
    assert isinstance(r, dict)
    assert r["japi_response"] == cmd
