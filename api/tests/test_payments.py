from fastapi.testclient import TestClient
from ..controllers import payments as controller
from ..main import app
import pytest
from ..models import payments as model

client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_payment(db_session):
    payment_data = {
        "order_id": 1,
        "card_last_four": "1234",
        "transaction_status": "Success",
        "payment_type": "Credit Card"
    }
    payment_object = model.Payment(**payment_data)
    created_payment = controller.create(db_session, payment_object)

    assert created_payment is not None
    assert created_payment.order_id == 1
    assert created_payment.transaction_status == "Success"