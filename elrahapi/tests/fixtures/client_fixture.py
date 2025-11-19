import pytest
from fastapi.testclient import TestClient

from ...myproject.main import app



@pytest.fixture
def client():
    client = TestClient(app)
    yield client
