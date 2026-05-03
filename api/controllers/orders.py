from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import orders as model
from ..models import order_details as detail_model
from ..models import menu_items as menu_model
from ..models import promotions as promo_model
from ..models import payments as payment_model
from datetime import datetime, timedelta

import uuid


def create(db: Session, request):
    total_price = 0.0

    for item in request.items:
        menu_item = db.query(menu_model.MenuItem).filter(menu_model.MenuItem.id == item.menu_item_id).first()
        if menu_item == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found.")

        for recipe in menu_item.recipes:
            resource = recipe.resource
            total_required = recipe.quantity_required * item.amount

            if resource.amount < total_required:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient ingredients. We do not have enough " + str(resource.name)
                )

            resource.amount = resource.amount - total_required

        total_price = total_price + (menu_item.price * item.amount)

    if request.promotion_id != None:
        promo = db.query(promo_model.Promotion).filter(promo_model.Promotion.id == request.promotion_id).first()
        if promo == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found!")
        if promo.expiration_date < datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promotion code has expired!")

        discount_amount = total_price * (promo.discount_percentage / 100.0)
        total_price = total_price - discount_amount

    generated_tracking_number = "TRK-" + str(uuid.uuid4())[:8].upper()

    new_order = model.Order(
        customer_id=request.customer_id,
        promotion_id=request.promotion_id,
        tracking_number=generated_tracking_number,
        order_status="Pending",
        total_price=total_price,
        order_type=request.order_type
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in request.items:
        new_detail = detail_model.OrderDetail(
            order_id=new_order.id,
            menu_item_id=item.menu_item_id,
            amount=item.amount
        )
        db.add(new_detail)

    db.commit()
    db.refresh(new_order)

    return new_order


def get_revenue(db: Session, start_date: str = None, end_date: str = None):
    query = db.query(payment_model.Payment).join(model.Order)
    query = query.filter(payment_model.Payment.transaction_status == "Completed")

    if start_date != None and end_date != None:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(model.Order.order_date >= start, model.Order.order_date < end)

    payments = query.all()

    total_revenue = 0.0
    paid_order_count = 0

    for payment in payments:
        paid_order_count = paid_order_count + 1
        total_revenue = total_revenue + payment.amount

    return {"total_orders": paid_order_count, "total_revenue": total_revenue}



def track_order(db: Session, tracking_number: str):
    item = db.query(model.Order).filter(model.Order.tracking_number == tracking_number).first()
    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking number not found!")
    return {"tracking_number": item.tracking_number, "order_status": item.order_status}


def read_all(db: Session, start_date: str = None, end_date: str = None):
    query = db.query(model.Order)

    if start_date != None:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(model.Order.order_date >= start)

    if end_date != None:
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(model.Order.order_date < end)

    result = query.all()
    return result


def read_one(db: Session, item_id):
    item = db.query(model.Order).filter(model.Order.id == item_id).first()
    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    return item

def update(db: Session, item_id, request):
    item = db.query(model.Order).filter(model.Order.id == item_id)

    if item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")

    update_data = request.dict(exclude_unset=True)
    item.update(update_data, synchronize_session=False)
    db.commit()

    return item.first()
