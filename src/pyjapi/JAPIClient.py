#!/usr/bin/env python3
"""JAPI Client in Python."""

import json
import logging as log
import socket
import sys
import typing as t
import uuid


class JAPIClient():
    """Connect and interact with arbitrary libJAPI-based backend."""

    def __init__(
        self,
        address: t.Tuple[str, int] = ('localhost', 1234),
        timeout: int = 3,
        request_no: t.Union[int, bool] = False,
    ):
        """Create new JAPIClient object.

        Args:
            address: Tuple of host (str) and port (int). Defaults to ('localhost', 1234).
            timeout: Timeout for requests in seconds. Defaults to 5.
            request_no:
                Whether to include japi request number.
                If a positive integer is given, request number starts at given integer and will increment with each message.
                If `True` is given, :py:func:`uuid.uuid4` is used to generate a random request number with 6 characters.


        """
        self._request_no = request_no
        self.last_request = None
        self.address = address
        try:
            self.sock = socket.create_connection(self.address)
            self.sock.settimeout(timeout)
            self.sockfile = self.sock.makefile()
        except ConnectionError as e:
            self.sock = None
            raise (e)

    @property
    def request_no(self):
        if isinstance(self._request_no, bool):
            if self._request_no:
                return str(uuid.uuid4())[:6]
            return False
        elif isinstance(self._request_no, int):
            self._request_no += 1
            return self._request_no - 1

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

    def query(self, cmd: str, **kwargs) -> dict:
        """Query JAPI server and return response.
        
        If an error occured, an empty dictionary is returned.

        Returns:
            Response object
        """
        if self.sock is None:
            log.error('')
            return {}

        cmd_request = self._build_request(cmd, **kwargs)
        log.debug('> %s', json.dumps(cmd_request))

        json_cmd = json.dumps(cmd_request) + '\n'
        try:
            self.sock.sendall(json_cmd.encode())
            resp = self.sockfile.readline()
            log.debug('< %s', resp)
        except (
            socket.gaierror,
            ConnectionResetError,
            ConnectionAbortedError,
            ConnectionError,
        ):
            log.warning('%s:%d is not available', self.address[0], self.address[1])
            return {}
        except socket.timeout:
            log.info("Request Timeout!")
            return {}
        except Exception as e:
            log.info(str(e))
            return {}

        try:
            response = json.loads(resp)
        except json.JSONDecodeError as e:
            log.error('Cannot parse response: %s (%s)', resp, str(e))
            return {}

        return response

    def listen(self, service: str, n_pkg: int = 0):
        """Listen for *n* values of *service*.

        Args:
            service: name of push service
            n: number of values to receive (optional, defaults to 0)

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

    def _build_request(self, cmd, **kwargs):
        request = {'japi_request': cmd}
        if self.request_no:
            request['japi_request_no'] = self.request_no
        if kwargs:
            request['args'] = kwargs

        self.last_request = request
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
