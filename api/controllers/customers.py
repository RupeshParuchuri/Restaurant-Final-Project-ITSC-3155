from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import customers as model


def create(db: Session, request):
    new_item = model.Customer(
        name=request.name,
        email=request.email,
        phone_number=request.phone_number,
        address=request.address
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


def read_one(db: Session, item_id):
    item = db.query(model.Customer).filter(model.Customer.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found!"
        )

    return item


def update(db: Session, item_id, request):
    item = db.query(model.Customer).filter(model.Customer.id == item_id)

    if not item.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Id not found!"
        )

    update_data = request.dict(exclude_unset=True)
    item.update(update_data, synchronize_session=False)
    db.commit()

    return item.first()