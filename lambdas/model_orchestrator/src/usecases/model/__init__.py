import typing
from abc import ABC, abstractclassmethod

import pandas as pd
from web.settings import LOG_MODEL_DATA

from gateways.aws.kinesis_firehose.ml_model_tracking import \
    MLModelTrackingKinesisFirehoseGateway
from src.usecases.logging.mixin import LoggableMixin
from src.utils.context import EventContext, EventContextHolder
from src.utils.sync import non_wait


class ModelPredictor(ABC, LoggableMixin):
    model_name: str
    model_version: int
    _firehose_stream = MLModelTrackingKinesisFirehoseGateway()
    _loggable: bool = True

    @classmethod
    @abstractclassmethod
    def get_model_info(cls):
        pass

    @classmethod
    @abstractclassmethod
    def get_columns(cls):
        pass

    @classmethod
    def rename_columns(cls, X, columns):
        new_columns = list(X.columns)
        old_columns = list(columns)
        missing = list(set(old_columns) - set(new_columns))
        if new_columns != old_columns:
            if len(new_columns) >= len(old_columns):
                try:
                    X = X[old_columns]
                except:
                    raise ValueError(
                        "The columns has changed. Please check missing collumns {}".format(missing)
                    )
            else:
                missing = list(set(old_columns) - set(new_columns))
                raise ValueError(
                    "The number of columns has decreased, from {} to {}. Missing columns {}".format(
                        len(old_columns), len(new_columns), missing
                    )
                )
        return X

    @classmethod
    def log_input(cls, input_data: pd.DataFrame, event_context: EventContext):
        data_w_index = input_data.copy().reset_index().to_dict(orient="records")
        cls.info(
            "Input",
            data={
                "input": data_w_index,
                "model_name": cls.model_name,
                "model_verion": cls.model_version,
            },
        )
        if LOG_MODEL_DATA and cls._loggable:
            cls._firehose_stream.send_data(
                model_name=cls.model_name,
                model_version=cls.model_version,
                event_type="model_input",
                data=data_w_index,
                metadata=event_context,
            )

    @classmethod
    def log_output(cls, output_data: typing.Any, event_context: EventContext):
        data_w_index = output_data.copy().reset_index().to_dict(orient="records")
        cls.info(
            "Output",
            event_context=event_context,
            data={
                "output": data_w_index,
                "model_name": cls.model_name,
                "model_verion": cls.model_version,
            },
        )
        if LOG_MODEL_DATA and cls._loggable:
            cls._firehose_stream.send_data(
                model_name=cls.model_name,
                model_version=cls.model_version,
                event_type="model_output",
                data=data_w_index,
                metadata=event_context,
            )

    @classmethod
    def predict(cls, input_data: pd.DataFrame) -> pd.DataFrame:
        event_context: EventContext = EventContextHolder.get()
        input_data = cls.treat_input_data(input_data)
        result_pd = cls._predict(input_data, event_context)
        event_context: EventContext = EventContextHolder.get()
        non_wait(cls.log_output(result_pd, event_context))
        return result_pd

    @classmethod
    @abstractclassmethod
    def _predict(cls, input_data: pd.DataFrame, event_context: EventContext):
        pass

    @classmethod
    @abstractclassmethod
    def _predict_proba(cls, input_data: pd.DataFrame, event_context: EventContext):
        pass

    @classmethod
    def treat_input_data(cls, input_data: pd.DataFrame) -> pd.DataFrame:
        columns = cls.get_columns()
        event_context: EventContext = EventContextHolder.get()
        if columns is not None:
            input_data = cls.rename_columns(input_data, columns)
        non_wait(cls.log_input(input_data, event_context))
        return input_data

    @classmethod
    def predict_proba(cls, input_data: pd.DataFrame, desired_column=1) -> pd.DataFrame:
        assert (
            desired_column <= 1
        ), f"desired column ({desired_column}) needs to be lesser equal than 2"
        event_context: EventContext = EventContextHolder.get()
        input_data = cls.treat_input_data(input_data)
        result = cls._predict_proba(input_data, event_context)
        result_pd = result[[f"prediction_{desired_column}"]]
        result_pd.rename({f"prediction_{desired_column}": "prediction"}, axis=1, inplace=True)
        non_wait(cls.log_output(result_pd, event_context))
        return result_pd
