import json
import typing

from boto3_type_annotations.firehose import Client

from src.devices.aws.base import BaseAwsDevice
from src.usecases.logging.mixin import LoggableMixin


class FirehoseClient(BaseAwsDevice, LoggableMixin):
    _aws_client_name: str = "firehose"
    _client: Client

    def put_dict_record(self, stream_name: str, body: typing.Dict[str, str]):
        self.put_json_record(stream_name=stream_name,
                             json_body=json.dumps(body))

    def put_record(self, stream_name: str, json_body: str):
        try:
            self.get_client().put_record(
                DeliveryStreamName=stream_name, Record={
                    "Data": json_body + "\n"}
            )

        except Exception as error:
            self.exception("Exception trying to put record in kinesis", error)
