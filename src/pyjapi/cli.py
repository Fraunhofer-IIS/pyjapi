#!/usr/bin/env python3
"""Command Line Interface for `~pyjapi.JAPIClient`."""

import json
import logging as log
import os
import sys

import click

try:
    from pyjapi import JAPIClient, util, err
except ImportError:  # support execution without proper installation for now
    from JAPIClient import JAPIClient
    import util
    import err

CTX_SETTINGS = dict(auto_envvar_prefix="JAPI")

HOST = os.getenv("JAPI_HOST", 'localhost')
PORT = int(os.getenv("JAPI_PORT", 1234))

# JAPIClient instance used for autocompletion, as click.ctx doesn't exist yet
try:
    J = JAPIClient((HOST, PORT))
except ConnectionError as e:
    J = None


def service_completer(ctx, args, incomplete):
    if J:
        services = J.list_push_services()
        if incomplete:
            services = [s for s in services if s.startswith(incomplete)]
        return services
    return []


def format_completer(ctx, args, incomplete):
    formats = [(fmt, desc) for fmt, desc in util.SUPPORTED_FORMATS.items()]
    if incomplete:
        formats = [fmt for fmt in formats if fmt[0].startswith(incomplete)]
    return formats


def format_callback(ctx, param, value):
    if value in util.SUPPORTED_FORMATS:
        util.FORMAT = value
    else:
        click.secho(
            f'{value} is not a supported format. Supported formats are: {", ".join(util.SUPPORTED_FORMATS)}',
            fg='red'
        )
    return value

@click.group(invoke_without_command=True, context_settings=CTX_SETTINGS)
@click.option(
    '-h',
    '--host',
    default='localhost',
    allow_from_autoenv=True,
    help='JAPI server hostname or ip',
    type=click.STRING,
    show_default=True,
)
@click.option(
    '-p',
    '--port',
    default=1234,
    allow_from_autoenv=True,
    help='JAPI server port',
    type=click.INT,
    show_default=True,
)
@click.option(
    '-f',
    '--format',
    default='concise',
    allow_from_autoenv=True,
    help='Output format of JAPI messages',
    autocompletion=format_completer,
    type=click.STRING,
    show_default=True,
    callback=format_callback,
    expose_value=False
)
@click.option(
    '-v',
    '--verbose',
    count=True,
    default=0,
    help='Increase verbosity of output.',
    type=click.INT,
)
@click.pass_context
def cli(ctx, host, port, verbose):
    """User & Command Line Friendly JAPI Client."""

    # If no command is given, print help and exit
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())
        exit(0)

    # Configure logger
    log.root.handlers = []
    log.basicConfig(
        stream=sys.stdout,
        level=[log.WARN, log.INFO, log.DEBUG][verbose] if 0 <= verbose < 2 else log.DEBUG,
        format='%(message)s',
    )
    log.info(f'Talking to {host}:{port}')
    try:
        ctx.obj = JAPIClient(address=(host, port))
    except ConnectionError as e:
        click.secho(f"{host}:{port} is not available!", fg='red')
        exit(1)


@cli.command()
@click.argument('service', default='push_temperature', autocompletion=service_completer)
@click.argument('n', default=0, type=click.INT)
@click.pass_context
def listen(ctx, service, n):
    """Listen for values of push service.

    If no SERVICE is given, SERVICE defaults to 'push_temperature' (available in libjapi-demo).
    For a list of available SERVICEs, use

        $ japi list

    By default, values are continuously received until either server or client closes the
    connection. Provide a positive integer for N to stop listening after N values have been
    received.

    """
    for response in ctx.obj.listen(service, n):
        click.echo(util.rformat(response))


@cli.command()
@click.pass_context
def list(ctx):
    """List available push services."""
    click.echo(util.rformat(ctx.obj.list_push_services(unpack=False)))


@cli.command()
@click.argument('cmd')
@click.argument('parameters', nargs=-1)
@click.option('-r', '--raw', is_flag=True, default=False, help='print raw response')
@click.pass_context
def request(ctx, cmd, parameters, raw):
    """Issue individual JAPI request.

    CMD is the JAPI Command (e.g. get_temperature) followed by any additional PARAMETERS.
    Parameters might be key-value-pairs in the form: key=value

    Examples: Subscribe to push_temperature service using `japi request`

        $ japi request japi_pushsrv_subscribe service=push_temperature

    """
    # Convert tuple of parameter list into dict: ('foo', 'bar=1') -> {'foo': '', 'bar': '1'}
    parameters = {p.split('=')[0]: p.split('=')[1] if '=' in p else '' for p in parameters}

    log.info(util.rformat(ctx.obj._build_request(cmd, **parameters)))
    response = ctx.obj.query(cmd, **parameters)
    if response:
    if raw:
        util.FORMAT = 'none'
    click.echo(util.rformat(response))
    else:
        click.secho("No response received!", fg='red')


if __name__ == '__main__':
    cli()
