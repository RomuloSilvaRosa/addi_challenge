import typing

from boto3 import Session
from boto3 import session as boto3session

from src.devices.aws.base.credentials import Credentials

BASE_SESSION = boto3session.Session()


def get_session(cred: typing.Union[typing.Dict, Credentials] = {}):
    credentials_raw = Credentials.from_dict_or_os(cred).to_dict(filter_data=True)
    credentials = {k: v for k, v in credentials_raw.items() if v is not None}
    if len(credentials):
        return Session(**credentials)
    return BASE_SESSION
