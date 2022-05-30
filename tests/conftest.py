import pytest
from fastapi.testclient import TestClient

from counter_app.main import get_app


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("ENABLE_METRICS", "false")
    return get_app()


@pytest.fixture
def client(app):
    return TestClient(app)
