from sqlalchemy.orm import Session
from ..models import menu_items as model


def search_menu_items(db: Session, category=None, min_price=None, max_price=None, name=None):
    query = db.query(model.MenuItem)

    if category:
        query = query.filter(model.MenuItem.food_category == category)

    if min_price:
        query = query.filter(model.MenuItem.price >= min_price)

    if max_price:
        query = query.filter(model.MenuItem.price <= max_price)

    if name:
        query = query.filter(model.MenuItem.name.ilike(f"%{name}%"))

    return query.all()