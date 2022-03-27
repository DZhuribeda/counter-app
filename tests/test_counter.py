def test_counter_reset(client):
    response = client.put("/counter/test/")
    assert response.status_code == 200
    assert response.json()["value"] == 0


def test_counter_increment(client):
    response = client.post("/counter/test/")
    assert response.status_code == 200
    assert response.json()["value"] == 1


def test_counter_get(client):
    response = client.get("/counter/test/")
    assert response.status_code == 200
    assert response.json()["value"] == 1
