import logging as log
import pathlib
import subprocess
from time import sleep

import pytest

from pyjapi import JAPIClient
from pyjapi.lib import convert

root = pathlib.Path(__file__).parent.parent


@pytest.fixture(scope="session", autouse=True)
def server():
    libjapi_build_dir = root / "ext" / "libjapi-demo" / "build"
    server = libjapi_build_dir / "demo-static"
    port = 1234
    proc = subprocess.Popen(
        [server, str(port)],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    # wait for server to be ready
    sleep(0.1)

    yield

    proc.kill()


@pytest.fixture
def client():
    try:
        client = JAPIClient()
    except Exception:
        pytest.xfail("No backend available!")
    yield client


@pytest.mark.parametrize(
    "cmd",
    [
        "japi_pushsrv_list",
        "japi_pushsrv_subscribe",
        "japi_pushsrv_unsubscribe",
    ],
)
def test_pushsrv_commands(client, cmd):
    r = client.query(cmd)
    log.info(r)
    assert isinstance(r, dict)
    assert r["japi_response"] == cmd


@pytest.mark.parametrize(
    "value,expected",
    [
        ("some_string", "some_string"),
        ("false", False),
        ("1000", 1000),
        ("1.2", 1.2),
        ("1e4", 10000.0),
        ("-inf", float("-inf")),
    ],
)
def test_type_inference(value, expected):
    """Test type inference is working."""
    result = convert(value)
    assert result == expected
