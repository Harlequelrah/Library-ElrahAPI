from datetime import datetime

import pytest
from elrahapi.testclass.elrahtest import ElrahTest

from ..my.settings.models_metadata import Base, database


class TestUser(ElrahTest):

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

    def test_should_create_user(self, client, fake_user, expected_user_value: dict):
        response = client.post("/users", json=fake_user)
        expected_user_value = self._update_expected_value(
            expected_value=expected_user_value
        )
        assert response.status_code == 201
        assert response.json() == expected_user_value

    def test_should_get_user_after_creation(
        self,
        client,
        fake_test_user,
        expected_user_value: dict,
        fake_access_token: str,
    ):
        headers = self._add_token_to_headers(
            token=fake_access_token, token_type="access_token"
        )
        response_get = client.get(
            f"/users/{expected_user_value['id']}", headers=headers
        )
        assert response_get.status_code == 200
        assert response_get.json() == expected_user_value

    def test_should_patch_user_after_creation(
        self,
        client,
        fake_test_user,
        expected_user_value: dict,
        fake_access_token: str,
    ):
        headers = self._add_token_to_headers(
            token=fake_access_token, token_type="access_token"
        )
        update_data = {"firstname": "Updated Name"}
        response_update = client.patch(
            f"/users/{expected_user_value['id']}", json=update_data, headers=headers
        )
        assert response_update.status_code == 200
        assert response_update.json()["firstname"] == update_data["firstname"]
        assert response_update.json()["id"] == expected_user_value["id"]

    def test_should_update_user_after_creation(
        self,
        client,
        fake_test_user,
        fake_update_user,
        expected_user_value: dict,
        fake_access_token: str,
    ):
        headers = self._add_token_to_headers(
            token=fake_access_token, token_type="access_token"
        )
        response_update = client.patch(
            f"/users/{expected_user_value['id']}",
            json=fake_update_user,
            headers=headers,
        )
        assert response_update.status_code == 200
        assert response_update.json()["email"] == fake_update_user["email"]
        assert response_update.json()["firstname"] == fake_update_user["firstname"]
        assert response_update.json()["username"] == fake_update_user["username"]
        assert response_update.json()["lastname"] == fake_update_user["lastname"]
        assert response_update.json()["id"] == fake_test_user["id"]

    def test_should_delete_user_after_creation(
        self,
        client,
        fake_test_user,
        expected_user_value: dict,
        fake_access_token: str,
    ):
        headers = self._add_token_to_headers(
            token=fake_access_token, token_type="access_token"
        )
        response_delete = client.delete(
            f"/users/{expected_user_value['id']}", headers=headers
        )
        assert response_delete.status_code == 204
        response_get = client.get(
            f"/users/{expected_user_value['id']}", headers=headers
        )
        assert response_get.status_code == 404

    def test_should_get_all_users(
        self,
        client,
        fake_test_user,
        expected_user_value: dict,
        fake_access_token: str,
    ):
        headers = self._add_token_to_headers(
            token=fake_access_token, token_type="access_token"
        )
        response_get_all = client.get("/users", headers=headers)
        assert response_get_all.status_code == 200
        assert isinstance(response_get_all.json(), list)
        assert fake_test_user in response_get_all.json()
