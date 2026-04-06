from pydantic import BaseModel

class PaymentBase(BaseModel):
    order_id: int
    card_last_four: str
    transaction_status: str
    payment_type: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int

    class ConfigDict:
        from_attributes = True