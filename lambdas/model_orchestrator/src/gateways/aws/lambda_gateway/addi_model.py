import typing

from src.devices.aws.lambda_function import LambdaClient


class AddiChallengeModeleGateway:
    _lambda_name = "addi-challenge-model"
    _device = LambdaClient()

    @classmethod
    def invoke(cls, body:str) -> typing.Any:
        resp = cls._device.invoke(function_name=cls._lambda_name, body=body)
        return resp["prediction"]

