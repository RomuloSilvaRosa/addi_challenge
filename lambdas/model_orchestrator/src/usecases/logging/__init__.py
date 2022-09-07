import json
import logging
import re
import sys
import typing
from datetime import datetime as dt


def _get_klass_name(klass: typing.Any) -> str:
    # Simple and effective
    return re.sub(r"|".join(map(re.escape, ["<class", "'", ">", " "])), "", str(klass))


_LOGGER = logging.getLogger('main_logger')
_LOGGER.setLevel(logging.INFO)




class JsonLogger(logging.LoggerAdapter):
    version: str = "NOTDEFINED"

    @classmethod
    def set_version(cls, version: str):
        cls.version = version

    def __init__(self, klass=None):
        self.logger = _LOGGER
        self.klass_name = _get_klass_name(klass)

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            _msg = dict(
                severity=logging.getLevelName(level),
                logmessage=msg,
                logger=self.klass_name,
                loggerName=self.logger.name,
                logdate=dt.utcnow().isoformat(),
                applicationVersion=self.version,
            )
            _msg["extra"] = kwargs.pop("data", None)

            if level == logging.ERROR and kwargs.get("exc_info"):
                args = tuple()
                fmt = logging.Formatter()
                _exc = sys.exc_info()
                _msg["stackTrace"] = fmt.formatException(_exc)

                kwargs["exc_info"] = False
            msg = json.dumps(_msg)
            self.logger.log(level, msg, *args, **kwargs)
