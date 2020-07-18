import json


class ApiGwEventParser:
    def __init__(self, event):
        self._event = event
        self.user_id = None
        self.token = None
        self.path = None
        self.method = None
        self.body = None
        self.headers = None

    def parse(self):
        self.user_id = self._event["requestContext"]["authorizer"]["principalId"]
        self.token = self._event["headers"]["Authorization"].split()[1]
        self.path = self._event["path"]
        self.method = self._event["httpMethod"]
        self.body = json.loads(self._event.get("body", "{}")) if self._event["body"] is not None else None


def base_response(status_code: int, dict_body=None, cors=True):
    headers = {"Content-Type": "application/json"}
    if cors is True:
        headers["Access-Control-Allow-Origin"] = "*"
    response_dict = dict(statusCode=status_code, headers=headers)
    if dict_body is not None and isinstance(dict_body, dict):
        response_dict["body"] = json.dumps(dict_body)

    return response_dict