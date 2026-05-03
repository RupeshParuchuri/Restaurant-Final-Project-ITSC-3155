from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import recipes as model


def create(db: Session, request):
    new_item = model.Recipe(
        menu_item_id=request.menu_item_id,
        resource_id=request.resource_id,
        quantity_required=request.quantity_required
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def read_all(db: Session):
    result = db.query(model.Recipe).all()
    return result


def read_one(db: Session, menu_item_id: int):
    items = db.query(model.Recipe).filter(model.Recipe.menu_item_id == menu_item_id).all()

    # check if the list is empty
    if len(items) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe for this menu item not found!")
    return items


def delete(db: Session, menu_item_id: int):
    items = db.query(model.Recipe).filter(model.Recipe.menu_item_id == menu_item_id)
    if items.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe for this menu item not found!")

    items.delete(synchronize_session=False)
    db.commit()
    return {"message": "recipe deleted"}