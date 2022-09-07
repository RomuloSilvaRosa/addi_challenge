import decimal
from datetime import datetime as dt
from decimal import Context
from typing import Any, Dict

from src.devices.aws.dynamo import DynamoClient

ctx = Context(prec=38)


def un_replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = un_replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = un_replace_decimals(obj[k])
        return obj
    elif isinstance(obj, float):
        return ctx.create_decimal_from_float(obj)
    else:
        return obj


def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


class CreditCardFeatureStoreGateway:
    _table_name = "feature-store-credit-card"
    _device = DynamoClient()
    _pk_name = "id"
    _table = None

    @classmethod
    def get_table(cls):
        if cls._table is None:
            resource = cls._device.get_resource()
            cls._table = resource.Table(cls._table_name)
        return cls._table

    @classmethod
    def get_data(cls, id: int) -> Dict[str, Any]:
        table = cls.get_table()
        res = table.get_item(Key={cls._pk_name: id})
        return replace_decimals(res.get(
            "Item"
        ))

    @classmethod
    def insert_data(cls, id: int, data: Dict[str, Any]) -> None:
        table = cls.get_table()
        attributes = data.copy()
        attributes[cls._pk_name] = id
        attributes["_created_at"] = str(dt.utcnow())
        d = un_replace_decimals(attributes)
        table.put_item(Item=d)
