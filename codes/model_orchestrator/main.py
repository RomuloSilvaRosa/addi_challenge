"""Lambda function to connect to database base a
"""
from src.entities.base import BaseModel
from src.gateways.aws.kinesis_firehose.ml_model_tracking import (
    EventType,
    MLModelTrackingKinesisFirehoseGateway,
)
from src.usecases.logging import JsonLogger


class ExpectedModelEvent(BaseModel):
    model_name: str
    model_version: int


class ExpectedClientEvent(BaseModel):
    id: int


class ExpectedEvent(BaseModel):
    model: ExpectedModelEvent
    client: ExpectedClientEvent


def handler(event, _):

    log = JsonLogger()
    log.info(event)
    event_obj: ExpectedEvent = ExpectedEvent(**event)
    model = event_obj.model
    client = event_obj.client
    MLModelTrackingKinesisFirehoseGateway.send_data(
        model.model_name, model.model_version, EventType.MODEL_INPUT, []
    )
    # client_cpf = ClientRepository(session).get(event["body"].get('cpf'))
    return None
