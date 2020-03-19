from subprocess import run, CompletedProcess


def test_execution_via_module():
    r: CompletedProcess = run(["python", "-m", "pyjapi"], capture_output=True)
    assert r.returncode == 0
    assert r.stdout.decode().startswith("Usage: japi [OPTIONS] COMMAND [ARGS]...")
    assert r.stderr.decode() == ''


def test_direct_execution():
    r: CompletedProcess = run(["./src/pyjapi/cli.py"], capture_output=True)
    assert r.returncode == 0
    assert r.stdout.decode().startswith("Usage: japi [OPTIONS] COMMAND [ARGS]...")
    assert r.stderr.decode() == ''
