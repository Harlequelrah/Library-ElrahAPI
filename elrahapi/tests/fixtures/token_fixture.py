import pytest
from elrahapi.authentication.token import TokenType

from ...myproject.main import authentication


@pytest.fixture
def fake_access_token():
    access_token = authentication.create_token(
        data={"sub": "test"}, token_type=TokenType.ACCESS_TOKEN
    )
    return access_token


@pytest.fixture
def fake_refresh_token():
    refresh_token = authentication.create_token(
        data={"sub": "test"}, token_type=TokenType.REFRESH_TOKEN
    )
    return refresh_token


@pytest.fixture
def auth_response(fake_test_user, client, credentials):
    login_response = client.post("/auth/login", json=credentials)
    return {
        "login_response": login_response.json(),
        "fake_test_user": fake_test_user,
    }
