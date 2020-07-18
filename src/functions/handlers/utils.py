import hashlib

from handlers.backend.secrets import get_api_key_secret


class ApiKeysManager:
    def __init__(self):
        pass

    @staticmethod
    def generate_api_key(organization_id: str):
        salt = get_api_key_secret()
        return hashlib.sha256(organization_id.encode() + salt.encode()).hexdigest()

    @staticmethod
    def validate_api_key(organization_id: str, api_key: str):
        salt = get_api_key_secret()
        return api_key == hashlib.sha256(organization_id.encode() + salt.encode()).hexdigest()
