import typing

from boto3.resources.base import ServiceResource
from botocore.client import BaseClient

from src.devices.aws.base.connector import AWSConnector
from src.devices.aws.base.credentials import Credentials
from src.utils import singleton


class BaseAwsDevice(metaclass=singleton):
    _aws_client_name: str
    _client: BaseClient = None
    _session = None
    _resource: ServiceResource = None

    def __init__(self, aws_credentials: typing.Union[typing.Dict, Credentials] = {}, **kwargs):
        self._session = AWSConnector.get_session(aws_credentials)

    def get_client(self):
        if self._client is None:
            self._client = self._session.client(self._aws_client_name)

        return self._client

    def get_resource(self):
        if self._resource is None:
            self._resource = self._session.resource(self._aws_client_name)

        return self._resource
