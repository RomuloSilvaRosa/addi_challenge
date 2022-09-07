import json
import typing
from dataclasses import dataclass
from http import HTTPStatus


@dataclass
class ErrorField:
    name: str
    error_type: str
    message: str

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return dict(name=self.name, errorType=self.error_type, message=self.message)


class HTTPException(Exception):
    http_status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    message: str = None

    def to_json(self):
        return json.dumps(self.to_dict())

class ValidationError(HTTPException):
    fields: typing.List[ErrorField]
    http_status: HTTPStatus = HTTPStatus.UNPROCESSABLE_ENTITY
    message: str = "Error in validation schema"

    def __init__(self, fields: typing.List[ErrorField]):
        self.fields = fields

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        _fields = list()
        for item in self.fields:
            _fields.append(item.to_dict())
        return dict(message=self.message, fields=_fields)
