from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import order_details as model

def read_all(db: Session):
    result = db.query(model.OrderDetail).all()
    return result

def read_one(db: Session, item_id):
    item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    return item
