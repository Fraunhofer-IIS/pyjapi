import json

DIM = "\033[2m"
Y = YELLOW = "\033[33m"
G = GREEN = "\033[92m"
B = BLUE = "\033[94m"
DEFAULT = "\033[39m"
X = RESET = "\033[0m"
FORMAT = 'user'

prefix = lambda r: '> ' if 'japi_request' in r else '< '
rtype = lambda r: [k for k in r if k not in ('japi_request_no', 'data', 'args')][0]
color = lambda r: GREEN if rtype(r) == 'japi_request' else YELLOW
"""Print requests in GREEN, responses and push values in YELLOW."""

SUPPORTED_FORMATS = {
    'nice': 'my favorite',
    'concise': 'like nice, but more concise',
    'indent': 'indented json with color',
    'color': 'requests and responses have different colors',
    'none': 'no formatting at all'
}


def rprint(r, *args, **kwargs):
    '''Pretty-print JAPI packages.'''
    print(rformat(r), *args, **kwargs)


def rformat(r) -> str:
    if FORMAT in ['nice', 'pretty', 'concise']:
        o = prefix(r)
        o += Y + r[rtype(r)] + X  # japi command
        # args
        o += '(' + ', '.join(f'{G}{k}{X}={B}{json.dumps(v)}{X}' for k, v in r.get('args', {}).items()) + ')'
        # put data in brackets, removing the need for newlines in format
        if FORMAT == 'concise' and 'args' not in r:
            o = o[:-2]  # remove empty brackets again
            o += '(' + ', '.join(f'{G}{k}{X}={B}{json.dumps(v)}{X}' for k, v in r.get('data', {}).items()) + ')'
        # japi request number
        o += f'  {DIM}# {r["japi_request_no"]}{X}' if 'japi_request_no' in r else ''
        # data
        if not (FORMAT == 'concise' and 'args' not in r):
            o += '\n  ' if 'data' in r else ''
            o += '\n  '.join(f'{G}{k}{X}={B}{json.dumps(v)}{X}' for k, v in r.get('data', {}).items())
    elif FORMAT in ['indent', 'json']:
        o = color(r) + json.dumps(r, indent=2) + X
    elif FORMAT in ['color']:
        o = color(r) + json.dumps(r) + X
    else:
        o = json.dumps(r)
    return o
