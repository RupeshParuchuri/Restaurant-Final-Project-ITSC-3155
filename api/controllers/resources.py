from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import resources as model


def create(db: Session, request):
    new_item = model.Resource(
        name=request.name,
        amount=request.amount,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def read_all(db: Session):
    result = db.query(model.Resource).all()
    return result


def read_one(db: Session, item_id):
    item = db.query(model.Resource).filter(model.Resource.id == item_id).first()
    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    return item


def update(db: Session, item_id, request):
    item = db.query(model.Resource).filter(model.Resource.id == item_id)
    if item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

    update_data = request.dict(exclude_unset=True)
    item.update(update_data, synchronize_session=False)
    db.commit()
    return item.first()


def delete(db: Session, item_id):
    item = db.query(model.Resource).filter(model.Resource.id == item_id)
    if item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

    item.delete(synchronize_session=False)
    db.commit()
    return {"message": "deleted"}