import pytest
from fastapi.testclient import TestClient

from counter_app.main import get_app


@pytest.fixture
def client():
    app = get_app()
    return TestClient(app)
