from fastapi.testclient import TestClient
from ..controllers import promotions as controller
from ..main import app
import pytest
from ..models import promotions as model
from datetime import datetime, timedelta

client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_promotion(db_session):
    future_date = datetime.now() + timedelta(days=30)
    promo_data = {
        "promotion_code": "SAVE20",
        "expiration_date": future_date,
        "discount_percentage": 20.0
    }

    promo_object = model.Promotion(**promo_data)
    created_promo = controller.create(db_session, promo_object)

    assert created_promo is not None
    assert created_promo.promotion_code == "SAVE20"
    assert created_promo.discount_percentage == 20.0