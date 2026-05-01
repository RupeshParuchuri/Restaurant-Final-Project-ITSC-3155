from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import payments as model


def create(db: Session, request):
    new_item = model.Payment(
        order_id=request.order_id,
        card_last_four=request.card_last_four,
        transaction_status=request.transaction_status,
        payment_type=request.payment_type
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


def read_one(db: Session, item_id):
    item = db.query(model.Payment).filter(model.Payment.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found!"
        )

    return item