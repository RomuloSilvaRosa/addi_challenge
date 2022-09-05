from typing import Any, Dict, List

from src.devices.aws.dynamo import DynamoClient
from src.utils.sync import non_wait


class ConsumerFeatureStoreGateway:
    _table_name = "feature-store-user-poc"
    _device = DynamoClient()
    _pk_name = "user_id"
    _range_key = "poc_id"
    _table = None

    @classmethod
    def get_table(cls):
        if cls._table is None:
            resource = cls._device.get_resource()
            cls._table = resource.Table(cls._table_name)
        return cls._table

    @classmethod
    def get_data(cls, user_id: str, poc_ids: List[int]) -> Dict[str, Any]:
        resource = cls._device.get_resource()
        keys = [{cls._pk_name: user_id, cls._range_key: x} for x in poc_ids]
        return (resource.batch_get_item(RequestItems={cls._table_name: {"Keys": keys}}))[
            "Responses"
        ][cls._table_name]


non_wait(ConsumerFeatureStoreGateway.get_data("1", [1]))
