from datetime import datetime

import pytest
from elrahapi.testclass.elrahtest import ElrahTest
from elrahapi.utility.utils import update_expected_value_dates

from ..myproject.settings.models_metadata import Base, database


class TestAuthentication(ElrahTest):

    @classmethod
    def setup_class(cls):
        database.env = "test"

    @classmethod
    def teardown_class(cls):
        database.env = "dev"

    def setup_method(self, method):
        try:
            database.create_tables(target_metadata=Base.metadata)
        except Exception as e:
            print(f"Error during table creation: {e}")

    def teardown_method(self, method):
        database.drop_tables(target_metadata=Base.metadata)

    def test_should_login_user(self, client, fake_test_user, credentials):
        response = client.post("/auth/login", json=credentials)
        assert response.status_code == 200

    def test_should_login_user_by_swagger(self, client, fake_test_user, credentials):
        response = client.post("/auth/tokenUrl", data=credentials)
        assert response.status_code == 200

    def test_should_not_create_user_with_existing_email(
        self, client, fake_test_user, fake_user
    ):
        response_duplicate = client.post("/users", json=fake_user)
        assert response_duplicate.status_code == 400

    def test_should_read_current_user(
        self,
        client,
        auth_response,
        expected_user_value: dict,
    ):
        login_response = auth_response["login_response"]
        headers = {"Authorization": f"Bearer {login_response['access_token']}"}
        response_current_user = client.get("/auth/read-current-user", headers=headers)
        response_current_user_json = response_current_user.json()
        response_current_user_json["user_roles"] = []
        response_current_user_json["user_privileges"] = []
        assert response_current_user.status_code == 200
        expected_user_value = update_expected_value_dates(expected_user_value)
        assert response_current_user_json == expected_user_value

    def test_should_read_user_by_sub(
        self,
        client,
        fake_test_user,
        fake_access_token,
        expected_user_value: dict,
    ):
        headers = self._add_token_to_headers(
            token=fake_access_token, token_type="access_token"
        )
        response_current_user = client.get(
            f"/auth/read-one-user/{fake_test_user["email"]}", headers=headers
        )
        response_user = response_current_user.json()
        response_user["user_roles"] = []
        response_user["user_privileges"] = []
        assert response_current_user.status_code == 200
        expected_user_value = update_expected_value_dates(expected_user_value)
        assert response_user == expected_user_value

    def test_should_change_user_state(
        self,
        client,
        auth_response,
    ):
        fake_test_user = auth_response["fake_test_user"]
        login_response = auth_response["login_response"]
        headers = {"Authorization": f"Bearer {login_response['access_token']}"}
        response_change_state = client.put(
            f"/auth/change-user-state/{fake_test_user['id']}", headers=headers
        )
        assert response_change_state.status_code == 204
        response_get_user = client.get(
            f"/users/{fake_test_user['id']}", headers=headers
        )
        assert response_get_user.status_code == 200
        response_get_user_json = response_get_user.json()
        assert response_get_user_json["is_active"] is False

    def test_should_refresh_token(
        self,
        client,
        auth_response,
    ):
        login_response = auth_response["login_response"]
        headers = {
            "Authorization": f"Bearer {login_response['access_token']}",
        }
        response_refresh = client.post(
            "/auth/refresh-token",
            json={
                "refresh_token": login_response["refresh_token"],
                "token_type": "refresh_token",
            },
            headers=headers,
        )
        assert response_refresh.status_code == 200
        response_refresh_json = response_refresh.json()
        assert "access_token" in response_refresh_json
        assert response_refresh_json["token_type"] == "bearer"

    def test_should_change_password(
        self,
        client,
        auth_response,
        credentials,
    ):
        fake_test_user = auth_response["fake_test_user"]
        login_response = auth_response["login_response"]
        headers = {
            "Authorization": f"Bearer {login_response['access_token']}",
        }
        new_password = "NewStrongPassword1!"
        response_change_password = client.post(
            "/auth/change-password",
            json={
                "username": fake_test_user["username"],
                "current_password": credentials["password"],
                "new_password": new_password,
            },
            headers=headers,
        )
        assert response_change_password.status_code == 204
        response_login_new = client.post(
            "/auth/login",
            json={
                "username": fake_test_user["username"],
                "password": new_password,
            },
        )
        assert response_login_new.status_code == 200
