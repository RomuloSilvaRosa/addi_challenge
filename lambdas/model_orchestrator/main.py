"""Lambda function to connect to database base a
"""
import logging

from src.entities.base import BaseModel
from src.usecases.logging import JsonLogger
from src.usecases.model_store import ModelStore


class ExpectedModelEvent(BaseModel):
    model_name: str
    model_version: int


class ExpectedClientEvent(BaseModel):
    id: int


class ExpectedEvent(BaseModel):
    model: ExpectedModelEvent
    client: ExpectedClientEvent


logging.basicConfig(level=logging.INFO)


def handler(event, _):

    log = JsonLogger()
    log.info({"input": event})
    event_obj: ExpectedEvent = ExpectedEvent(**event)
    model = event_obj.model
    client = event_obj.client
    desired_model = ModelStore.get_model(model.model_name, model.model_version)
    f = desired_model.get_features(client.id)
    r = desired_model.predict(f)
    log.info({"prediction": r})
    desired_model.store_on_evaluation_store(client.id, f, r)

    return {"prediction": r}
