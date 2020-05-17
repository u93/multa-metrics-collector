import json


def base_response(status_code: int, dict_body=None):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }
    response_dict = dict(statusCode=status_code, headers=headers)
    if dict_body is not None and isinstance(dict_body, dict):
        response_dict["body"] = json.dumps(dict_body)

    return response_dict
