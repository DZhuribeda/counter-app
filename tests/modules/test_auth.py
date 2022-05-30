import pytest
import jwt
from jwt.utils import from_base64url_uint
import json
from cryptography.hazmat.primitives.asymmetric import rsa


@pytest.fixture
def user_id():
    return "user_id"


@pytest.fixture
def token(user_id):
    with open("./keys/jwks.json", "r") as f:
        jwks = json.load(f)
    numbers = jwks["keys"][0]
    public_numbers = rsa.RSAPublicNumbers(e=from_base64url_uint(numbers["e"]), n=from_base64url_uint(numbers["n"]))
    private_numbers = rsa.RSAPrivateNumbers(
        p=from_base64url_uint(numbers["p"]),
        q=from_base64url_uint(numbers["q"]),
        d=from_base64url_uint(numbers["d"]),
        dmp1=from_base64url_uint(numbers["dp"]),
        dmq1=from_base64url_uint(numbers["dq"]),
        iqmp=from_base64url_uint(numbers["qi"]),
        public_numbers=public_numbers,
    )
    private_key = private_numbers.private_key(backend=None)
    return jwt.encode({'sub': {'id': user_id}}, private_key, algorithm='RS256', headers={'kid': 'test-str'})

def test_decode_token(app, token, user_id):
    service = app.container.authentication_service()
    user = service.decode_token(token)
    assert user
    assert user.id == user_id
