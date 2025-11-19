import pytest
from elrahapi.utility.utils import exclude_dates_from_json, update_expected_value_dates

from .client_fixture import client


@pytest.fixture
def fake_user():
    return {
        "password": "@StrongPassword1",
        "email": "user@example.com",
        "username": "Harlequelrah",
        "lastname": "SMITH",
        "firstname": "jean-francois",
    }


@pytest.fixture
def expected_user_value():
    return {
        "date_deleted": None,
        "is_deleted": False,
        "id": 1,
        "is_active": True,
        "attempt_login": 0,
        "user_roles": [],
        "user_privileges": [],
        "email": "user@example.com",
        "username": "Harlequelrah",
        "lastname": "SMITH",
        "firstname": "jean-francois",
    }


@pytest.fixture
def fake_update_user():
    return {
        "email": "user_updated@example.com",
        "username": "testupdate",
        "lastname": "UPDATE",
        "firstname": "jean-update",
    }


@pytest.fixture
def fake_test_user(client, fake_user, expected_user_value):
    user_create = client.post("/users", json=fake_user)
    user_create_json = user_create.json()
    # user_create_json = update_expected_value_dates(user_create.json())
    # user_create_json = exclude_dates_from_json(user_create.json())
    if (
        user_create.status_code == 201
        and user_create_json == update_expected_value_dates(expected_user_value)
    ):
        return user_create.json()
    return None


@pytest.fixture
def credentials(fake_user):
    return {"username": fake_user["username"], "password": fake_user["password"]}


