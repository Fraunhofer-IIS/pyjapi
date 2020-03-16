import json

DIM = "\033[2m"
Y = YELLOW = "\033[33m"
G = GREEN = "\033[92m"
B = BLUE = "\033[94m"
DEFAULT = "\033[39m"
X = RESET = "\033[0m"
FORMAT = 'concise'
"""One of :py:data:`SUPPORTED_FORMATS`."""

PREFIX_SENT = '> '
PREFIX_RCV = '< '


def rtype(r: dict) -> str:
    """Return japi message type (e.g. 'japi_request', 'japi_response').
    
    >>> rtype({'japi_response': 'get_temperature'})
    'japi_response'

    >>> rtype({})
    Traceback (most recent call last):
    ...
    ValueError: empty japi message does not have a type!

    """
    if r:
        try:
            return [k for k in r if k not in ('japi_request_no', 'data', 'args')][0]
        except IndexError:
            raise ValueError("unknown japi response type: %s" % str(r))
    else:
        raise ValueError("empty japi message does not have a type!")


def _prefix(r: dict) -> str:
    return PREFIX_SENT if rtype(r) == 'japi_request' else PREFIX_RCV


def _color(r: dict):
    """Return `GREEN` for japi_requests, `YELLOW` otherwise (e.g. japi_responses and push values)."""
    return GREEN if rtype(r) == 'japi_request' else YELLOW


SUPPORTED_FORMATS = {
    'nice': 'my favorite',
    'concise': 'like nice, but more concise',
    'indent': 'indented json with color',
    'color': 'requests and responses have different colors',
    'values-only': 'display only response values',
    'none': 'no formatting at all'
}
"""All formats supported by :func:`rformat`.

Examples:

    .. command-output:: japi mock 

    >>> r = {'japi_response': 'japi_pushsrv_list', 'data': {'services': ['push_temperature', 'push_counter']}}
    >>> print(rformat(r))
    >>> print(rformat(r))

"""


def rprint(r, *args, **kwargs):
    '''Pretty-print JAPI packages.'''
    print(rformat(r), *args, **kwargs)


def rformat(r, format: str = None) -> str:
    """Format japi message *r* according to :py:data:`FORMAT`."""
    if not r:
        return ''

    if format is None:
        fmt = FORMAT
    elif format not in SUPPORTED_FORMATS:
        log.warning("%s is not a supported format!", format)
        fmt = FORMAT
    else:
        fmt = format

    if fmt in ['nice', 'pretty', 'concise']:
        o = _prefix(r)
        o += Y + r[rtype(r)] + X  # japi command
        # args
        o += '(' + ', '.join(f'{G}{k}{X}={B}{json.dumps(v)}{X}' for k, v in r.get('args', {}).items()) + ')'
        # put data in brackets, removing the need for newlines in format
        if fmt == 'concise' and 'args' not in r:
            o = o[:-2]  # remove empty brackets again
            o += '(' + ', '.join(f'{G}{k}{X}={B}{json.dumps(v)}{X}' for k, v in r.get('data', {}).items()) + ')'
        # japi request number
        o += f'  {DIM}# {r["japi_request_no"]}{X}' if 'japi_request_no' in r else ''
        # data
        if not (fmt == 'concise' and 'args' not in r):
            o += '\n  ' if 'data' in r else ''
            o += '\n  '.join(f'{G}{k}{X}={B}{json.dumps(v)}{X}' for k, v in r.get('data', {}).items())
    elif fmt in ['indent', 'json']:
        o = _color(r) + json.dumps(r, indent=2) + X
    elif fmt in ['color']:
        o = _color(r) + json.dumps(r) + X
    elif fmt in ['values-only']:
        o = json.dumps(r.get("data"))
    else:
        o = json.dumps(r)
    return o
