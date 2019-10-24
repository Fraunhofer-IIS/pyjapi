#!/usr/bin/env python3
"""JAPI Client in Python."""
import json
import logging as log
import socket
import sys

import click


class JAPIClient():
    """Connect and interact with arbitrary libJAPI-based backend."""

    def __init__(self, address=('localhost', 1234), timeout=5):
        """Create new JAPIClient object.

        Args:
            address (tuple, optional): Tuple of host (str) and port (int). Defaults to ('localhost', 1234).
            timeout (int, optional): Timeout for requests in seconds. Defaults to 5.

        """
        self.address = address
        try:
            self.sock = socket.create_connection(self.address)
            self.sock.settimeout(timeout)
            self.sockfile = self.sock.makefile()
        except ConnectionError as e:
            self.sock = None
            log.error(str(e))

    def list_push_services(self):
        """List available JAPI push services."""
        if self.sock is not None:
            return self.query('japi_pushsrv_list').get('data', {}).get('services', [])
        return []

    def query(self, cmd: str, **kwargs):
        """Query JAPI server and return response."""
        if self.sock is None:
            log.error('')
            return {}

        cmd_request = {'japi_request': cmd}
        if kwargs:
            cmd_request['args'] = kwargs
        log.debug('-> %s', cmd_request)

        json_cmd = json.dumps(cmd_request) + '\n'
        try:
            self.sock.sendall(json_cmd.encode())
            resp = self.sockfile.readline()
            log.debug('<- %s', resp)

        except (
            socket.gaierror,
            ConnectionResetError,
            ConnectionAbortedError,
            ConnectionError,
        ):
            log.warning('%s:%d is not available', self.address[0], self.address[1])
            return False
        except Exception as e:
            log.warning(str(e))
            return False

        try:
            response = json.loads(resp)
        except json.JSONDecodeError as e:
            log.error('Cannot parse response: %s (%s)', resp, str(e))
            return False
        except Exception as e:
            log.error(str(e))
            return False

        return response

    def listen(self, service, n_pkg=0):
        """Listen for *n* values of *service*.

        Args:
            service (str): name of push service
            n (int): number of values to receive (optional, defaults to 0)

        """
        if self.sock is None:
            log.warning('Not connected!')
            return {}
        self._subscribe(service)
        log.info(
            f"Listening for {str(n_pkg)+' ' if n_pkg > 0 else ''}{service} package{'s' if n_pkg != 1 else ''}..."
        )
        for n, line in enumerate(self.sock.makefile(), start=1):
            yield json.loads(line).get('data')
            if n_pkg and n >= n_pkg:
                break

    def _subscribe(self, service='counter'):
        """Subscribe to JAPI push service."""
        log.info('Subscribing to %s push service.', service)
        return self.query('japi_pushsrv_subscribe', service=service)

    def _unsubscribe(self, service='counter'):
        """Unsubscribe from JAPI push service."""
        log.info('Unsubscribing from %s push service.', service)
        return self.query('japi_pushsrv_unsubscribe', service=f'push_{service}')

    def __del__(self):
        """Close socket upon deletion."""
        if self.sock:
            if self.sockfile:
                self.sockfile.close()
            self.sock.close()


@click.group(invoke_without_command=True)
@click.option(
    '--host',
    envvar='JAPI_HOST',
    default='127.0.0.1',
    help='JAPI server hostname or ip',
    type=click.STRING,
)
@click.option(
    '-p',
    '--port',
    envvar='JAPI_PORT',
    default=1234,
    help='JAPI server port',
    type=click.INT,
)
@click.option('-v', '--verbose', count=True, default=0, help='Increase verbosity of output.')
@click.pass_context
def _cli(ctx, host, port, verbose):
    if verbose > 0:
        log.root.handlers = []  # Delete existing log handlers
        log.basicConfig(
            stream=sys.stdout,
            level=[log.WARN, log.INFO, log.DEBUG][verbose],
            format='%(message)s',
        )
    log.info(f'Talking to {host}:{port}')
    ctx.obj = JAPIClient(address=(host, port))


@_cli.command()
@click.argument('service', default='counter')
@click.argument('duration', default=0, type=click.INT)
@click.pass_context
def _listen(ctx, service, duration):
    for response in ctx.obj.listen(service, duration):
        click.echo(json.dumps(response))


@_cli.command()
@click.argument('cmd')
@click.option('-r', '--raw', is_flag=True, default=False, help='print raw response')
@click.pass_context
def _request(ctx, cmd, raw):
    response = ctx.obj.query(cmd)
    if raw:
        click.echo(json.dumps(response))
    else:
        if 'japi_response' in response:
            response.pop('japi_response')
        response = '\n'.join([f'{key}={val}' for key, val in response.get('data').items()])
    click.echo(response)


if __name__ == '__main__':
    _cli()
