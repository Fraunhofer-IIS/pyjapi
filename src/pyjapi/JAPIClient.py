#!/usr/bin/env python3
"""JAPI Client in Python."""

import json
import logging as log
import socket
import sys

JAPI_COMMANDS = {
    "push_services_list": {
        "japi_request": "japi_pushsrv_list"
    },
    "push_services_subscribe": {
        "japi_request": "japi_pushsrv_subscribe",
        "args": {
            "service": "push_temperature"
        }
    },
    "push_services_unsubscribe": {
        "japi_request": "japi_pushsrv_unsubscribe",
        "args": {
            "service": "push_temperature"
        }
    }
}


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
            raise (e)

    def list_push_services(self, unpack=True):
        """List available JAPI push services.
        
        Examples:
            
            >>> JAPIClient().list_push_services()
            ["push_temperature"]
            
            >>> JAPIClient().list_push_services(unpack=False)
            {'japi_response': 'japi_pushsrv_list', 'data': {'services': ['push_temperature']}}
            
        Returns: List of available push services
        
        """
        r = []
        if self.sock is not None:
            r = self.query('japi_pushsrv_list')
            if unpack:
                r = r.get('data', {}).get('services', [])
        return r

    def query(self, cmd: str, **kwargs):
        """Query JAPI server and return response."""
        if self.sock is None:
            log.error('')
            return {}

        cmd_request = self._build_request(cmd, **kwargs)
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
            yield json.loads(line)
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

    @staticmethod
    def _build_request(cmd, **kwargs):
        request = {'japi_request': cmd}
        if kwargs:
            request['args'] = kwargs
        return request

    def __del__(self):
        """Close socket upon deletion."""
        if self.sock:
            if self.sockfile:
                self.sockfile.close()
            self.sock.close()


if __name__ == "__main__":
    from cli import cli
    cli()
