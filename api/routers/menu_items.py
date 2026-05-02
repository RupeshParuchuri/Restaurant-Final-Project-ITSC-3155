from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..controllers import menu_items as controller
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/menuitems",
    tags=["Menu Items"]
)

@router.get("/search")
def search_menu_items(
    category: str | None = Query(None),
    min_price: float | None = Query(None),
    max_price: float | None = Query(None),
    name: str | None = Query(None),
    db: Session = Depends(get_db)
):
    return controller.search_menu_items(
        db=db,
        category=category,
        min_price=min_price,
        max_price=max_price,
        name=name
    )