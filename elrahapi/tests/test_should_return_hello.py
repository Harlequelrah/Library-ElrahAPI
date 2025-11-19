from fastapi.testclient import TestClient

from ..myproject.main import app

client = TestClient(app)


def test_should_return_hello():
    response = client.get("/")
    expected_value = {"message": "hello"}
    assert response.status_code == 200
    assert response.json() == expected_value
