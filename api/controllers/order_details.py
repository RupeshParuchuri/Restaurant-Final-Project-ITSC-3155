from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import order_details as model


def create(db: Session, request):
    new_item = model.OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        amount=request.amount
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


def read_all(db: Session):
    result = db.query(model.OrderDetail).all()
    return result


def read_one(db: Session, item_id):
    item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found!"
        )

    return item


def update(db: Session, item_id, request):
    item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)

    if not item.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found!"
        )

    update_data = request.dict(exclude_unset=True)
    item.update(update_data, synchronize_session=False)
    db.commit()

    return item.first()


def delete(db: Session, item_id):
    item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)

    if not item.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found!"
        )

    item.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)