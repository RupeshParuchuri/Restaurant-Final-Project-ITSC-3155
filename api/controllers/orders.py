from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders as model
from ..models import promotions as promo_model
from datetime import datetime


def create(db: Session, request):
    final_price = request.total_price

    if request.promotion_id:
        promo = db.query(promo_model.Promotion).filter(promo_model.Promotion.id == request.promotion_id).first()
        if not promo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found!")
        if promo.expiration_date < datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promotion code has expired!")

        final_price = request.total_price * (1 - (promo.discount_percentage / 100.0))

    new_item = model.Order(
        customer_id=request.customer_id,
        promotion_id=request.promotion_id,
        tracking_number=request.tracking_number,
        order_status=request.order_status,
        total_price=final_price,
        order_type=request.order_type
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


def read_all(db: Session):
    result = db.query(model.Order).all()
    return result


def read_one(db: Session, item_id):
    item = db.query(model.Order).filter(model.Order.id == item_id).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

    return item


def update(db: Session, item_id, request):
    item = db.query(model.Order).filter(model.Order.id == item_id)

    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

    update_data = request.dict(exclude_unset=True)
    item.update(update_data, synchronize_session=False)
    db.commit()

    return item.first()


def delete(db: Session, item_id):
    item = db.query(model.Order).filter(model.Order.id == item_id)

    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

    item.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)