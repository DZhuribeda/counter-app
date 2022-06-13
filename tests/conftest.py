from unittest.mock import Mock
from uuid import uuid4
from httpx import AsyncClient
import pytest
from fastapi.testclient import TestClient
import jwt
from jwt.utils import from_base64url_uint
import json
from cryptography.hazmat.primitives.asymmetric import rsa

from counter_app.main import get_app
from counter_app.modules.auth.dependencies import get_optional_user
from counter_app.modules.auth.service import AuthenticationService
from counter_app.modules.auth.model import User


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("ENABLE_METRICS", "false")
    return get_app()


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def token_factory():
    def create(user_id):
        with open("./keys/jwks.json", "r") as f:
            jwks = json.load(f)
        numbers = jwks["keys"][0]
        public_numbers = rsa.RSAPublicNumbers(
            e=from_base64url_uint(numbers["e"]), n=from_base64url_uint(numbers["n"])
        )
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
        return jwt.encode(
            {"sub": {"id": user_id}},
            private_key,
            algorithm="RS256",
            headers={"kid": "test-str"},
        )

    return create


@pytest.fixture
def user_id():
    return uuid4().hex


@pytest.fixture
def another_user_id():
    return uuid4().hex


@pytest.fixture
def authorized_user(app, user_id):
    with app.container.authentication_service.override(Mock(AuthenticationService)):
        app.dependency_overrides[get_optional_user] = lambda: User(id=user_id)
        yield


@pytest.fixture
def another_authorized_user(app, another_user_id):
    with app.container.authentication_service.override(Mock(AuthenticationService)):
        app.dependency_overrides[get_optional_user] = lambda: User(id=another_user_id)
        yield
