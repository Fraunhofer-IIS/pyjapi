#!/usr/bin/env python3
"""JAPI Client in Python."""
import json
import logging as log
import socket
import sys

import click

__version__ = '0.2.0'


class JAPIClient():

    def __init__(self, conn_str=("localhost", 1234), timeout=5):
        self.conn_str = conn_str
        try:
            self.sock = socket.create_connection(self.conn_str)
            self.sock.settimeout(timeout)
            self.sockfile = self.sock.makefile()
        except ConnectionError as e:
            self.sock = None
            log.error(str(e))

    def list_push_services(self):
        """List available JAPI push services."""
        if self.sock is not None:
            return self.query("japi_pushsrv_list").get("services", [])
        return []

    def query(self, cmd: str, timeout=10, **kwargs):
        """Query JAPI server and return response."""
        if self.sock is None:
            log.error("")
            return {}
        log.debug("Use socket timeout %s", timeout)

        cmd_request = {"japi_request": cmd}
        if kwargs:
            cmd_request['args'] = kwargs
        log.debug("-> %s", cmd_request)

        json_cmd = json.dumps(cmd_request) + "\n"
        try:
            self.sock.sendall(json_cmd.encode())
            resp = self.sockfile.readline()
            log.debug("<- %s", resp)

        except (
            socket.gaierror,
            ConnectionResetError,
            ConnectionAbortedError,
            ConnectionError,
        ):
            log.warning("%s:%d is not available", self.conn_str[0], self.conn_str[1])
            return False
        except Exception as e:
            log.warning(str(e))
            return False

        try:
            response = json.loads(resp)
        except json.JSONDecodeError as e:
            log.error("Cannot parse response: %s (%s)", resp, str(e))
            return False
        except Exception as e:
            log.error(str(e))
            return False

        return response

    def listen(self, service, n_pkg=0):
        """Listen for JAPI messages."""
        if self.sock is None:
            log.warning("Not connected!")
            return {}
        self._subscribe(service)
        log.info(
            f"Listening for {str(n_pkg)+' ' if n_pkg > 0 else ''}{service} package{'s' if n_pkg != 1 else ''}..."
        )
        for n, line in enumerate(self.sock.makefile(), start=1):
            yield json.loads(line).get('data')
            if n_pkg and n >= n_pkg:
                break

    def get(self, service):
        """Return first message for *service*."""
        for val in self.listen(service, n_pkg=1):
            return val

    def _subscribe(self, service="counter"):
        """Subscribe to JAPI push service."""
        log.info("Subscribing to %s push service.", service)
        return self.query(
            "japi_pushsrv_subscribe", service=service if service.startswith("push_") else f"push_{service}"
        )

    def _unsubscribe(self, service="counter"):
        """Unsubscribe from JAPI push service."""
        log.info("Unsubscribing from %s push service.", service)
        return self.query("japi_pushsrv_unsubscribe", service=f"push_{service}")

    def __del__(self):
        """Close socket upon deletion."""
        self.sockfile.close()
        self.sock.close()


@click.group(invoke_without_command=True)
@click.option(
    "--host",
    envvar="JAPI_HOST",
    default="127.0.2.0",
    help="JAPI server hostname or ip",
    type=click.STRING,
)
@click.option(
    "-p",
    "--port",
    envvar="JAPI_PORT",
    default=1234,
    help="JAPI server port",
    type=click.INT,
)
@click.option("-v", "--verbose", count=True, default=0, help="Increase verbosity of output.")
@click.pass_context
def cli(ctx, host, port, verbose):
    if verbose > 0:
        log.root.handlers = []  # Delete existing log handlers
        log.basicConfig(
            stream=sys.stdout,
            level=[log.WARN, log.INFO, log.DEBUG][verbose],
            format="%(message)s",
        )
    log.info(f"Talking to {host}:{port}")
    ctx.obj = JAPIClient(conn_str=(host, port))


@cli.command()
@click.argument("service", default="counter")
@click.argument("duration", default=0, type=click.INT)
@click.pass_context
def listen(ctx, service, duration):
    # ctx.obj.listen(service, duration)
    for response in ctx.obj.listen(service, duration):
        click.echo(json.dumps(response))


@cli.command()
@click.argument("cmd")
@click.option("-r", "--raw", is_flag=True, default=False, help="print raw response")
@click.pass_context
def request(ctx, cmd, raw):
    response = ctx.obj.query(cmd)
    if raw:
        click.echo(json.dumps(response))
    else:
        if "japi_response" in response:
            response.pop("japi_response")
        response = "\n".join([f"{key}={val}" for key, val in response.get('data').items()])
    click.echo(response)


if __name__ == "__main__":
    cli()
