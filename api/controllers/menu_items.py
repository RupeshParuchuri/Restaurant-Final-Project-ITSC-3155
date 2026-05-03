from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import menu_items as model


def create(db: Session, request):
    new_item = model.MenuItem(
        name=request.name,
        price=request.price,
        calories=request.calories,
        food_category=request.food_category
    )

    # save to database
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def read_all(db: Session, category: str = None, min_calories: int = None, max_calories: int = None):
    query = db.query(model.MenuItem)

    if category != None:
        query = query.filter(model.MenuItem.food_category == category)

    if min_calories != None:
        query = query.filter(model.MenuItem.calories >= min_calories)

    if max_calories != None:
        query = query.filter(model.MenuItem.calories <= max_calories)

    result = query.all()
    return result


def read_one(db: Session, item_id):
    item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    return item


def update(db: Session, item_id, request):
    item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
    if item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

    update_data = request.dict(exclude_unset=True)
    item.update(update_data, synchronize_session=False)
    db.commit()
    return item.first()


def delete(db: Session, item_id):
    item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
    if item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

    item.delete(synchronize_session=False)
    db.commit()
    return {"message": "deleted"}

