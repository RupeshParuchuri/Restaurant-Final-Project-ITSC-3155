import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_revenue_endpoint():
    response = client.get("/orders/revenue")

    assert response.status_code == 200

    data = response.json()
    assert "total_orders" in data
    assert "total_revenue" in data
    assert isinstance(data["total_orders"], int)
    assert isinstance(data["total_revenue"], float)
