import typing
from abc import ABC, abstractclassmethod

from src.gateways.aws.dynamodb.credit_card_feature_store import \
    CreditCardFeatureStoreGateway
from src.gateways.aws.kinesis_firehose.ml_model_tracking import (
    MLModelTrackingKinesisFirehoseGateway, str_everything)
from src.gateways.aws.lambda_gateway.company_model import \
    companyshowcaseModeleGateway

ModelCatalog: typing.Dict[typing.Tuple[str, int], 'ModelStore'] = dict()


class ModelStore(ABC):
    name: str = None
    version: int = -1

    def __init_subclass__(cls):
        ModelCatalog[(cls.name, cls.version)] = cls

    @classmethod
    def get_model(cls, model_name: str, model_version: int) -> "ModelStore":
        return ModelCatalog.get((model_name, model_version))

    @abstractclassmethod
    def get_features(cls, pk: typing.Any):
        pass

    @abstractclassmethod
    def predict(cls, pk: typing.Any):
        pass

    @abstractclassmethod
    def store_on_evaluation_store(cls, pk: typing.Any, features: typing.Dict[str, typing.Any], prediction: typing.Any):
        pass


class companyshowcaseModel(ModelStore):
    name = 'company-showcase'
    version = 1

    @classmethod
    def get_features(cls, pk: typing.Any) -> typing.Dict[str, typing.Any]:
        features = CreditCardFeatureStoreGateway.get_data(pk) or {}
        return features

    @classmethod
    def predict(cls, features: typing.Dict[str, typing.Any]):
        response = companyshowcaseModeleGateway.invoke(features)
        return response

    @classmethod
    def store_on_evaluation_store(cls, pk: typing.Any, features: typing.Dict[str, typing.Any], prediction: typing.Any) -> None:
        kw = dict(features=features.copy())
        kw["pk"] = pk
        kw["prediction"] = prediction
        kw["model_name"] = cls.name
        kw['model_version'] = cls.version
        _kw = str_everything(kw)
        MLModelTrackingKinesisFirehoseGateway.send_data(
            **_kw
        )
