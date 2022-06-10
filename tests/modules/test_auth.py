import pytest


@pytest.fixture
def token(user_id, token_factory):
    return token_factory(user_id)


def test_decode_token(app, token, user_id):
    service = app.container.authentication_service()
    user = service.decode_token(token)
    assert user
    assert user.id == user_id
