from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db
from ..schemas.revenue import RevenueResponse

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)

@router.get("/revenue", response_model=RevenueResponse)
def get_revenue(start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    return controller.get_revenue(db, start_date=start_date, end_date=end_date)

@router.get("/track/{tracking_number}")
def track_order(tracking_number: str, db: Session = Depends(get_db)):
    return controller.track_order(db, tracking_number=tracking_number)

@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Order])
def read_all(start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    return controller.read_all(db, start_date=start_date, end_date=end_date)

@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, item_id=item_id, request=request)