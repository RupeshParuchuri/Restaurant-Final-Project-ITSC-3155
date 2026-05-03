from fastapi.testclient import TestClient
from ..controllers import menu_items as controller
from ..main import app
import pytest
from ..models import menu_items as model

client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_menu_item(db_session):
    menu_data = {
        "name": "Spicy Chicken Sandwich",
        "price": 8.99,
        "calories": 650,
        "food_category": "Spicy"
    }
    menu_object = model.MenuItem(**menu_data)
    created_item = controller.create(db_session, menu_object)

    assert created_item != None
    assert created_item.name == "Spicy Chicken Sandwich"
    assert created_item.food_category == "Spicy"