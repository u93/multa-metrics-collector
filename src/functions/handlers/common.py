import boto3


class Session:
    def __init__(self):
        self._user_session = boto3.session.Session()
        self.user_region = self._user_session.region_name


class Sts(Session):
    def __init__(self):
        Session.__init__(self)
        self._account_client = boto3.client("sts")
        self.account_id = self._account_client.get_caller_identity()["Account"]
