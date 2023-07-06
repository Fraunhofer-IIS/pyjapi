import json
import typing as t
import logging as log


class JAPIMessage(dict):
    def __init__(self, initdata=None):
        dict.__init__(self, initdata)

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def args(self) -> t.Dict[str, t.Any]:
        return self.get("args")

    def dumps(self, *args, **kwargs) -> str:
        return json.dumps(self, *args, **kwargs)


class JAPIResponse(JAPIMessage):
    """A Japi response message."""

    def __init__(self, initdata=None):
        super().__init__(initdata)
        assert "japi_response" in self

    @property
    def name(self) -> str:
        return self["japi_response"]

    @property
    def data(self) -> t.Dict[str, t.Any]:
        return self.get("data")

    @property
    def success(self) -> bool:
        return self.get("data", {}).get("JAPI_RESPONSE") == "success"


class JAPIRequest(JAPIMessage):
    """A JAPI request message."""

    def __init__(self, initdata):
        JAPIMessage.__init__(self, initdata=initdata)
        log.debug(f"JAPIRequest({initdata})")
        assert "japi_request" in self
