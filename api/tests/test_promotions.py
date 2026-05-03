from fastapi.testclient import TestClient
from ..controllers import promotions as controller
from ..main import app
import pytest
from datetime import datetime, timedelta
from ..schemas import promotions as promotion_schema

client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_promotion(db_session):
    future_date = datetime.now() + timedelta(days=30)

    promo_request = promotion_schema.PromotionCreate(
        promotion_code="SAVE20",
        expiration_date=future_date,
        discount_percentage=20.0
    )

    created_promo = controller.create(db_session, promo_request)

    assert created_promo.promotion_code == "SAVE20"
    assert created_promo.expiration_date == future_date
    assert created_promo.discount_percentage == 20.0


def test_read_promotion_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(Exception):
        controller.read_one(db_session, item_id=999)