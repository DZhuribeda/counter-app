from unittest.mock import Mock
from httpx import AsyncClient
import pytest
from fastapi.testclient import TestClient

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
def user_id():
    return "user_id"


@pytest.fixture
def authorized_user(app, user_id):
    with app.container.authentication_service.override(Mock(AuthenticationService)):
        app.dependency_overrides[get_optional_user] = lambda: User(id=user_id)
        yield
