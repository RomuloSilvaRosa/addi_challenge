from boto3_type_annotations.dynamodb import Client, ServiceResource

from src.devices.aws.base import BaseAwsDevice
from src.usecases.logging.mixin import LoggableMixin


class DynamoClient(BaseAwsDevice, LoggableMixin):
    _aws_client_name: str = "dynamodb"
    _client: Client
    _resource: ServiceResource
