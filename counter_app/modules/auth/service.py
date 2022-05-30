import jwt
from jwt import PyJWKClient

from .model import User

# TODO: rewrite from scratch to make async
class JWKClient(PyJWKClient):
    def fetch_data(self):
        data = super().fetch_data()
        for key in data['keys']:
            for wrong_key in set(key.keys()) - set(['kty', 'n', 'e', 'use', 'kid', 'alg']):
                key.pop(wrong_key, None)
        return data


class AuthenticationService:
    def __init__(self, jwks_client: JWKClient):
        self.jwks_client = jwks_client

    def _parse_header(self, header_value: str) -> dict:
        splitted_value = header_value.split(1)
        if len(splitted_value) != 2:
            return None
        return splitted_value[1]

    def decode_token(self, token: str) -> User | None:
        signing_key = self.jwks_client.get_signing_key_from_jwt(token)
        try:
            data = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"]
            )
        except jwt.InvalidTokenError:
            return None
        return User(
            id = data['sub']['id'],
        )
