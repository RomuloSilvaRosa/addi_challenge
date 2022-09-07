import json
import typing

from boto3_type_annotations.sagemaker_runtime import Client
from botocore.response import StreamingBody

from src.devices.aws.base import BaseAwsDevice


class LambdaClient(BaseAwsDevice):
    _client: Client
    _aws_client_name = "lambda"

    def invoke(self, function_name:str, body:typing.Union[typing.Dict, bytes]
    ) -> StreamingBody:
        if not isinstance(body, bytes):
            body = bytes(json.dumps(body), "utf-8")
        response = self.get_client().invoke(
        FunctionName=function_name,
        Payload=body
    )
        return json.loads(response["Payload"].read())
