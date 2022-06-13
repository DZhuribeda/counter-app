import random
import string
import pytest

from counter_app.modules.permissions.model import CounterRoles


@pytest.fixture
def counter_factory(user_id, app):
    async def create_counter(name):
        service = await app.container.counter.counter_service()
        counter = await service.create(name=name, owner_id=user_id)
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
    response = client.post("/api/v1/counters/", json={"name": "test"})
    assert response.status_code == 307
    assert response.headers.get("location").startswith("/api/v1/counters/")


@pytest.mark.usefixtures("authorized_user")
async def test_counter_get_list(async_client, counter):
    response = await async_client.get(f"/api/v1/counters/")
    assert response.status_code == 200, response.json()
    data = response.json()
    assert len(data["data"]) == 1
    fetched_counter = data["data"][0]
    assert fetched_counter["id"] == str(counter)
    assert fetched_counter["role"] == "admin"
    for key in ["ownerId", "name", "createdAt", "role"]:
        assert key in fetched_counter


@pytest.mark.usefixtures("authorized_user")
async def test_counter_get(async_client, counter):
    response = await async_client.get(f"/api/v1/counters/{counter}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(counter)
    assert data["role"] == "admin"
    for key in ["ownerId", "name", "createdAt", "role"]:
        assert key in data

@pytest.mark.usefixtures("authorized_user")
async def test_counter_delete(async_client, counter):
    response = await async_client.delete(f"/api/v1/counters/{counter}/")
    assert response.status_code == 204


@pytest.mark.usefixtures("authorized_user")
async def test_counter_put(async_client, counter):
    response = await async_client.put(
        f"/api/v1/counters/{counter}/", json={"name": "testing"}
    )
    assert response.status_code == 204


@pytest.mark.usefixtures("authorized_user")
async def test_counter_value_reset(async_client, counter):
    response = await async_client.put(f"/api/v1/counterValue/{counter}/")
    assert response.status_code == 200
    assert response.json()["value"] == 0


@pytest.mark.usefixtures("authorized_user")
async def test_counter_value_increment(async_client, counter):
    response = await async_client.post(f"/api/v1/counterValue/{counter}/")
    assert response.status_code == 200
    assert response.json()["value"] == 101


@pytest.mark.usefixtures("authorized_user")
async def test_counter_value_get(async_client, counter):
    response = await async_client.get(f"/api/v1/counterValue/{counter}/")
    assert response.status_code == 200
    assert response.json()["value"] == 100


@pytest.mark.usefixtures("another_authorized_user")
async def test_counter_unauthorized_for_another_user(async_client, counter):
    response = await async_client.get(f"/api/v1/counters/{counter}/")
    assert response.status_code == 403


async def test_counter_shared_for_another_user(
    async_client, counter, token_factory, user_id, another_user_id
):
    user_token = token_factory(user_id)
    another_user_token = token_factory(another_user_id)

    response = await async_client.get(
        f"/api/v1/counters/{counter}/",
        headers={"Authorization": f"Bearer {another_user_token}"},
    )
    assert response.status_code == 403

    response = await async_client.post(
        f"/api/v1/counters/{counter}/sharing/",
        json={"role": CounterRoles.READER.value, "user_id": another_user_id},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 204, response.json()

    response = await async_client.get(
        f"/api/v1/counters/{counter}/",
        headers={"Authorization": f"Bearer {another_user_token}"},
    )
    assert response.status_code == 200

    response = await async_client.get(
        f"/api/v1/counters/",
        headers={"Authorization": f"Bearer {another_user_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1


async def test_counter_shared_users(
    async_client, counter, token_factory, user_id, another_user_id
):
    user_token = token_factory(user_id)

    response = await async_client.post(
        f"/api/v1/counters/{counter}/sharing/",
        json={"role": CounterRoles.READER.value, "user_id": another_user_id},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 204, response.json()

    response = await async_client.get(
        f"/api/v1/counters/{counter}/sharing/",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200, response.json()


async def test_deleted_sharing_for_another_user(
    async_client, counter, token_factory, user_id, another_user_id
):
    user_token = token_factory(user_id)
    another_user_token = token_factory(another_user_id)

    response = await async_client.get(
        f"/api/v1/counters/{counter}/",
        headers={"Authorization": f"Bearer {another_user_token}"},
    )
    assert response.status_code == 403

    response = await async_client.post(
        f"/api/v1/counters/{counter}/sharing/",
        json={"role": CounterRoles.READER.value, "user_id": another_user_id},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 204, response.json()

    response = await async_client.get(
        f"/api/v1/counters/{counter}/",
        headers={"Authorization": f"Bearer {another_user_token}"},
    )
    assert response.status_code == 200

    response = await async_client.delete(
        f"/api/v1/counters/{counter}/sharing/{another_user_id}/",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 204, response.json()

    response = await async_client.get(
        f"/api/v1/counters/{counter}/",
        headers={"Authorization": f"Bearer {another_user_token}"},
    )
    assert response.status_code == 403
