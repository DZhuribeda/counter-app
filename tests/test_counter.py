import random
import string
import pytest

from counter_app.modules.counter.model import AccessModeEnum


@pytest.fixture
def counter_factory(user_id, app):
    async def create_counter(name):
        service = await app.container.counter.counter_service()
        counter = await service.create(
            name=name, access_mode=AccessModeEnum.PRIVATE, owner_id=user_id
        )
        await service.set_value(counter, 100)
        return counter

    return create_counter


@pytest.fixture
def counter_name():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(15))


@pytest.fixture
async def counter(counter_factory, counter_name):
    return await counter_factory(counter_name)


@pytest.mark.usefixtures("authorized_user")
def test_counter_create(client):
    response = client.post(
        "/api/v1/counter/", json={"name": "test", "access_mode": "private"}
    )
    assert response.status_code == 307
    assert response.headers.get("location").startswith("/api/v1/counter/")


@pytest.mark.usefixtures("authorized_user")
async def test_counter_get(async_client, counter):
    response = await async_client.get(f"/api/v1/counter/{counter}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(counter)
    for key in ["ownerId", "name", "accessMode", "createdAt"]:
        assert key in data


@pytest.mark.usefixtures("authorized_user")
async def test_counter_delete(async_client, counter):
    response = await async_client.delete(f"/api/v1/counter/{counter}/")
    assert response.status_code == 204


@pytest.mark.usefixtures("authorized_user")
async def test_counter_put(async_client, counter):
    response = await async_client.put(
        f"/api/v1/counter/{counter}/", json={"name": "testing", "access_mode": "public"}
    )
    assert response.status_code == 204


async def test_counter_value_reset(async_client, counter):
    response = await async_client.put(f"/api/v1/counterValue/{counter}/")
    assert response.status_code == 200
    assert response.json()["value"] == 0


async def test_counter_value_increment(async_client, counter):
    response = await async_client.post(f"/api/v1/counterValue/{counter}/")
    assert response.status_code == 200
    assert response.json()["value"] == 101


async def test_counter_value_get(async_client, counter):
    response = await async_client.get(f"/api/v1/counterValue/{counter}/")
    assert response.status_code == 200
    assert response.json()["value"] == 100
