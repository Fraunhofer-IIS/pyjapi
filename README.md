# pyjapi - Python JAPI Client

## Getting Started

```sh
pip install git+https://git01.iis.fhg.de/mkj/pyjapi
```

If the above method doesn't work for you, try to clone and install in-place like this:

```sh
$ git clone https://git01.iis.fhg.de/mkj/pyjapi
...
$ pip3 install -e pyjapi/.
```

## Usage

`japi [--host HOSTNAME] [--port N] [-v] (list|listen|request)`

## Examples

### Issue individual JAPI commands

- `japi request <JAPI_COMMAND>`

    ```sh
    (env) $ japi request get_temperature
    temperature=27.0
    unit=celsius

    (env) $ _
    ```

### List available push services

- `japi list`

    ```sh
    (env) $ japi list
    ['push_temperature']

    (env) $ _
    ```

### Listen to JAPI push services

- `japi listen <PUSH_SERVICE_NAME> <N_PACKAGES>`

    ```sh
    (env) $ japi listen push_temperature 3
    {"temperature": 39.09297426825681}
    {"temperature": 38.632093666488736}
    {"temperature": 38.0849640381959}

    (env) $ _
    ```
