import pytest
from fastapi.testclient import TestClient

from counter_app.main import get_app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv('ENABLE_METRICS', 'false')
    app = get_app()
    return TestClient(app)
