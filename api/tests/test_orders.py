from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_order_with_customer(db_session):
    order_data = {
        "customer_id": 1,
        "tracking_number": "TRK123",
        "total_price": 45.99,
        "order_type": "Takeout"
    }
    order_object = model.Order(**order_data)
    created_order = controller.create(db_session, order_object)

    assert created_order is not None
    assert created_order.customer_id == 1
    assert created_order.order_type == "Takeout"


def test_create_guest_order(db_session):
    order_data = {
        "customer_id": None,
        "tracking_number": "TRK456",
        "total_price": 25.00,
        "order_type": "Delivery"
    }
    order_object = model.Order(**order_data)
    created_order = controller.create(db_session, order_object)

    assert created_order is not None
    assert created_order.customer_id is None
    assert created_order.order_type == "Delivery"

def test_create_order(db_session):
    # Create a sample order
    order_data = {
        "customer_name": "John Doe",
        "description": "Test order"
    }

    order_object = model.Order(**order_data)

    # Call the create function
    created_order = controller.create(db_session, order_object)

    # Assertions
    assert created_order is not None
    assert created_order.customer_name == "John Doe"
    assert created_order.description == "Test order"
