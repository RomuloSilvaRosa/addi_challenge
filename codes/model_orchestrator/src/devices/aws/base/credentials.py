import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Credentials:
    aws_secret_access_key: str = field(default=None)
    aws_access_key_id: str = field(default=None)
    aws_session_token: str = field(default=None)
    aws_profile: str = field(default=None)
    region_name: str = field(default="us-east-1")

    @staticmethod
    def from_dict_or_os(obj: Any) -> "Credentials":
        def get_config(kwargs, get_first, get_second=None):
            if get_second is None:
                get_second = get_first.upper()
            return kwargs.get(get_first) or os.environ.get(get_second)

        credentials_raw = {
            "aws_secret_access_key": get_config(obj, "aws_secret_access_key"),
            "aws_access_key_id": get_config(obj, "aws_access_key_id"),
            "aws_profile": get_config(obj, "aws_profile"),
            "aws_session_token": get_config(obj, "aws_session_token"),
            "region_name": get_config(obj, "region_name", "AWS_REGION"),
        }
        credentials = {k: v for k, v in credentials_raw.items() if v is not None}
        return Credentials(**credentials)

    @staticmethod
    def from_dict(obj: Any) -> "Credentials":
        assert isinstance(obj, dict)
        aws_secret_access_key = obj.get("aws_secret_access_key")
        aws_access_key_id = obj.get("aws_access_key_id")
        aws_profile = obj.get("aws_profile")
        aws_session_token = obj.get("aws_session_token")
        region_name = obj.get("region_name")
        return Credentials(
            aws_secret_access_key, aws_access_key_id, aws_session_token, aws_profile, region_name
        )

    def to_dict(self, filter_data=True) -> dict:
        result: dict = {}
        result["aws_secret_access_key"] = self.aws_secret_access_key
        result["aws_access_key_id"] = self.aws_access_key_id
        result["aws_session_token"] = self.aws_session_token
        result["region_name"] = self.region_name
        result["profile_name"] = self.aws_profile
        if filter_data:
            result = {k: v for k, v in result.items() if v is not None}
        return result
