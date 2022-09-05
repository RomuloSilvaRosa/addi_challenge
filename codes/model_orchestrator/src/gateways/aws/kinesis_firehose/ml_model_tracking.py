from datetime import date
from datetime import datetime as dt
from enum import Enum
from typing import Any, Dict, List
from uuid import uuid4

from pydantic import Field

from src.devices.aws.kinesis import FirehoseClient
from src.entities.base import BaseModel

DataType = List[Dict[str, Any]]


class EventType(Enum):
    MODEL_INPUT = "model_input"
    MODEL_OUTPUT = "model_output"


class MLModelTrackingSchema(BaseModel):
    event_id: str
    model_name: str
    model_version: int
    event_type: EventType
    data: DataType
    created_at: dt = Field(default_factory=dt.now)
    created_date: date = Field(default_factory=date.today)


class MLModelTrackingKinesisFirehoseGateway:
    _stream_name = "evaluation-store-firehose-stream"
    _device = FirehoseClient()

    @classmethod
    def send_data(
        cls,
        model_name: str,
        model_version: int,
        event_type: EventType,
        data: DataType
    ) -> None:
        json_body = MLModelTrackingSchema(
            model_name=model_name,
            model_version=model_version,
            event_type=event_type,
            data=data,
            event_id=str(uuid4()),
        ).to_json(exclude_none=True)

        cls._device.put_record(cls._stream_name, json_body)
