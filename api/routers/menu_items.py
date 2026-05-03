from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from ..controllers import menu_items as controller
from ..schemas import menu_items as schema
from ..dependencies.database import get_db

router = APIRouter(tags=['Menu Items'], prefix="/menuitems")

@router.post("/", response_model=schema.MenuItem)
def create(request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

from typing import Optional

@router.get("/", response_model=list[schema.MenuItem])
def read_all(
    category: Optional[str] = None,
    min_calories: Optional[int] = None,
    max_calories: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return controller.read_all(db, category=category, min_calories=min_calories, max_calories=max_calories)

@router.get("/{item_id}", response_model=schema.MenuItem)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.MenuItem)
def update(item_id: int, request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.update(db=db, item_id=item_id, request=request)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)