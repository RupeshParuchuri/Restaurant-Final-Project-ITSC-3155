from fastapi.testclient import TestClient
from ..controllers import payments as controller
from ..main import app
import pytest
from ..schemas import payments as payment_schema

client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_payment(db_session):
    payment_request = payment_schema.PaymentCreate(
        order_id=1,
        amount=30.97,
        card_last_four="1234",
        transaction_status="Completed",
        payment_type="Credit Card"
    )

    created_payment = controller.create(db_session, payment_request)

    assert created_payment.order_id == 1
    assert created_payment.amount == 30.97
    assert created_payment.card_last_four == "1234"
    assert created_payment.transaction_status == "Completed"
    assert created_payment.payment_type == "Credit Card"