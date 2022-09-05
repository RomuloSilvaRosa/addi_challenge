import json
import typing

from pydantic import BaseModel as PydanticBaseModel
from pydantic import validate_model

from src.entities.exceptions import ErrorField, ValidationError


def _to_camel(string: str) -> str:
    result = string.split("_")
    result[1:] = [word.capitalize() for word in result[1:]]
    return "".join(result)


class BaseModel(PydanticBaseModel):
    def __init__(__pydantic_self__, **data):
        if typing.TYPE_CHECKING:
            __pydantic_self__.__dict__: typing.Dict[str, typing.Any] = {}
            __pydantic_self__.__fields_set__: "SetStr" = set()
        values, fields_set, validation_error = validate_model(__pydantic_self__.__class__, data)
        if validation_error:
            _fields = list()
            errors = validation_error.errors()
            for each_error in errors:
                _fields.append(
                    ErrorField(
                        name=each_error.get("loc")[0],
                        message=each_error.get("msg"),
                        error_type=each_error.get("type"),
                    )
                )
            raise ValidationError(_fields)
        object.__setattr__(__pydantic_self__, "__dict__", values)
        object.__setattr__(__pydantic_self__, "__fields_set__", fields_set)

    @classmethod
    def from_object(cls, obj: "BaseModel"):
        return cls(**obj.to_dict())

    def to_dict(self, *args, **kwargs) -> typing.Dict[str, typing.Any]:
        return self.dict(by_alias=True, *args, **kwargs)

    def to_json(self, *args, **kwargs) -> str:
        return self.json(by_alias=True)

    @classmethod
    def from_json(cls, data: str) -> "CamelPydanticMixin":
        try:
            _data = json.loads(data)
        except json.decoder.JSONDecodeError as exception:
            raise ValidationError(
                fields=[ErrorField(name="json", error_type=exception.msg, message=str(exception))]
            )
        return cls(**_data)


class CamelPydanticMixin(BaseModel):
    class Config:
        alias_generator = _to_camel

    def __init__(self, by_alias=True, **data: typing.Any) -> None:
        _data = dict()
        for key, value in data.items():
            if by_alias:
                key = self.Config.alias_generator(key)
            _data[key] = value
        super().__init__(**_data)
