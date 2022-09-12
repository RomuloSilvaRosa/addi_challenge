from datetime import date
from datetime import datetime as dt
from typing import Any, Dict, List
from uuid import uuid4

from pydantic import Field

from src.devices.aws.kinesis import FirehoseClient
from src.entities.base import BaseModel

DataType = Dict[str, str]


class MLModelTrackingSchema(BaseModel):
    event_id: str
    model_name: str
    model_version: str
    features: DataType
    prediction: str
    pk : str
    created_at: dt = Field(default_factory=dt.utcnow)

def str_everything(data):
    if isinstance(data, list):
        _l = list()
        for x in data:
            _l.append(str_everything(x))
        return _l
    elif isinstance(data, dict):
        _d = dict()
        for k, v in data.items():
            _d[k] = str_everything(v)
        return _d
    else:
        return str(data)
class MLModelTrackingKinesisFirehoseGateway:
    _stream_name = "evaluation-store-firehose-stream"
    _device = FirehoseClient()

    @classmethod
    def send_data(
        cls,
        model_name: str,
        model_version: int,
        features: DataType,
        prediction: str,
        pk : str
    ) -> None:
        json_body = MLModelTrackingSchema(
            model_name=model_name,
            model_version=model_version,
            features=features,
            prediction=prediction,
            pk=pk,
            event_id=str(uuid4()),
        ).to_json(exclude_none=False)

        cls._device.put_record(cls._stream_name, json_body)
