from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import recipes as controller
from ..schemas import recipes as schema
from ..dependencies.database import get_db

router = APIRouter(tags=['Recipes'], prefix="/recipes")

@router.post("/", response_model=schema.Recipe)
def create(request: schema.RecipeCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Recipe])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{menu_item_id}", response_model=list[schema.Recipe])
def read_one(menu_item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(menu_item_id=menu_item_id, db=db)

@router.delete("/{menu_item_id}")
def delete(menu_item_id: int, db: Session = Depends(get_db)):
    return controller.delete(menu_item_id=menu_item_id, db=db)