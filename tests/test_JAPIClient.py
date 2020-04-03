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


def test_type_inference(client):
    """Test type inference is working."""
    kwargs = {'str': 'string', 'bool': 'false', 'int': '1000', 'float': '1.2', 'float': '1e4', 'float': '-inf'}
    japi_request = client._build_request("command", **kwargs)
    assert isinstance(japi_request['args'], dict)
    for k, v in japi_request['args'].items():
        assert isinstance(v, eval(k))
