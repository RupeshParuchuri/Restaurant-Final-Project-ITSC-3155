from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import menu_items as menu_model
from ..schemas import orders as order_schema
from ..schemas import order_details as detail_schema

client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def setup_menu_item_query(db_session):
    menu_item = menu_model.MenuItem(
        id=1,
        name="Burger",
        price=15.50,
        calories=700,
        food_category="Entree"
    )
    menu_item.recipes = []

    db_session.query.return_value.filter.return_value.first.return_value = menu_item

    return menu_item


def test_create_order_with_customer(db_session):
    setup_menu_item_query(db_session)

    order_request = order_schema.OrderCreate(
        customer_id=1,
        promotion_id=None,
        order_type="Takeout",
        items=[
            detail_schema.OrderDetailCreate(
                menu_item_id=1,
                amount=2
            )
        ]
    )

    created_order = controller.create(db_session, order_request)

    assert created_order is not None
    assert created_order.customer_id == 1
    assert created_order.order_type == "Takeout"
    assert created_order.total_price == 31.00
    assert created_order.order_status == "Pending"


def test_create_guest_order(db_session):
    setup_menu_item_query(db_session)

    order_request = order_schema.OrderCreate(
        customer_id=None,
        promotion_id=None,
        order_type="Delivery",
        items=[
            detail_schema.OrderDetailCreate(
                menu_item_id=1,
                amount=1
            )
        ]
    )

    created_order = controller.create(db_session, order_request)

    assert created_order is not None
    assert created_order.customer_id is None
    assert created_order.order_type == "Delivery"
    assert created_order.total_price == 15.50


def test_create_order(db_session):
    setup_menu_item_query(db_session)

    order_request = order_schema.OrderCreate(
        customer_id=None,
        promotion_id=None,
        order_type="Takeout",
        items=[
            detail_schema.OrderDetailCreate(
                menu_item_id=1,
                amount=3
            )
        ]
    )

    created_order = controller.create(db_session, order_request)

    assert created_order is not None
    assert created_order.order_type == "Takeout"
    assert created_order.total_price == 46.50
    assert created_order.tracking_number is not None


def test_revenue_endpoint():
    response = client.get("/orders/revenue")

    assert response.status_code == 200

    data = response.json()
    assert "total_orders" in data
    assert "total_revenue" in data