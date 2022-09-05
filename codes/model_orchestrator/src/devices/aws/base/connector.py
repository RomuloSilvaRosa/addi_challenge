import typing

from boto3 import Session

from src.devices.aws.base.credentials import Credentials
from src.devices.aws.base.session import get_session


class AWSConnector:
    _session: Session = None
    _instances: list = list()

    @classmethod
    def get_session(cls, credentials: typing.Union[typing.Dict, Credentials] = {}) -> Session:
        for session, cred in cls._instances:
            if cred == credentials:
                return session
        session = get_session(credentials)
        cls._instances.append((session, credentials))
        return session
