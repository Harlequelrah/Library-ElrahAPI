import pytest
from fastapi.testclient import TestClient

from app.main import app



@pytest.fixture
def client():
    client = TestClient(app)
    yield client
