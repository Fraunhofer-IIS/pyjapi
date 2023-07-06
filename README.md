# pyjapi - Python JAPI Client

## Getting Started

Install from Gitlab's package registry directly:

```console
pip3 install pyjapi --index-url https://__token__:glpat-Ld7LCzjjjx32xFR3YNKG@git01.iis.fhg.de/api/v4/projects/5422/packages/pypi/simple
```

Alternatively, you might want to clone the project and go from there:

```console
git clone git@git01.iis.fhg.de:ks-ip-lib/software/pyjapi.git
pip install -e pyjapi/.
```

## Usage

`japi [--host HOSTNAME] [--port N] [--format FORMAT_NAME] [-v] (list|listen|request)`

## Examples

### Issue individual JAPI commands

- `japi request <JAPI_COMMAND>`

    ```console
    $ japi request get_temperature
    > get_temperature() #2a96d8
    < get_temperature() #2a96d8 --> temperature=17.0
    ```

- `japi request <COMMAND> [PARAMETERS]`

    ```console
    $ japi request get_temperature unit=kelvin
    > get_temperature(unit="kelvin") #02c6fa
    < get_temperature(unit="kelvin") #02c6fa --> temperature=290.0
    ```

### List available push services

- `japi list`

    ```console
    $ japi list
    > japi_pushsrv_list() #4fae82
    < japi_pushsrv_list() #4fae82 --> services=["push_temperature"]
    ```

### Listen to JAPI push services

- `japi listen <PUSH_SERVICE_NAME> <N_PACKAGES>`

    ```console
    $ japi listen push_temperature 3
    > japi_pushsrv_subscribe(service="push_temperature") #b71d22
    < push_temperature() --> temperature=24.833269096274833
    < push_temperature() --> temperature=25.414709848078964
    < push_temperature() --> temperature=25.912073600614352
    ```
