# pyjapi - Python JAPI Client

## Getting Started

```sh
(env) $ pip install git+https://git01.iis.fhg.de/mkj/pyjapi
(env) $ japi request get_temperature
temperature=27.0
unit=celsius
(env) $ japi listen temperature
{
    "temperature": 39.09297426825681,
    "japi_pushsrv": "push_temperature"
}
{
    "temperature": 38.632093666488736,
    "japi_pushsrv": "push_temperature"
}
{
    "temperature": 38.0849640381959,
    "japi_pushsrv": "push_temperature"
}
(env) $ _
```
