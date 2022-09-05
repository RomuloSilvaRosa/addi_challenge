import json
import typing

from boto3_type_annotations.sagemaker_runtime import Client
from botocore.response import StreamingBody

from src.devices.aws.base import BaseAwsDevice


class SagemakerRuntimeClient(BaseAwsDevice):
    _client: Client
    _aws_client_name = "sagemaker-runtime"

    def invoke_endpoint(
        self,
        endpoint_name: str,
        body: typing.Union[typing.Dict, bytes],
        content_type="application/json",
        accept="application/json",
    ) -> StreamingBody:
        if not isinstance(body, bytes):
            body = bytes(json.dumps(body), "utf-8")
        response = self._client.invoke_endpoint(
            EndpointName=endpoint_name, Body=body, Accept=accept
        )
        return response["Body"]
