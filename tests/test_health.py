import pytest


def test_healthz(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == "OK"


def test_readyz_ok(client):
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["healthy"] == True


@pytest.fixture
def invalid_redis(monkeypatch):
    def mock_redis_ping(self):
        raise Exception("Redis is down")

    monkeypatch.setattr("aioredis.Redis.ping", mock_redis_ping)


@pytest.mark.usefixtures("invalid_redis")
def test_readyz_false(client):
    response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json()["healthy"] == False
