from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail, OrderDetailCreate

class OrderBase(BaseModel):
    customer_id: Optional[int] = None
    promotion_id: Optional[int] = None
    order_type: str = "Takeout"

class OrderCreate(OrderBase):
    items: List[OrderDetailCreate]

class Order(OrderBase):
    id: int
    tracking_number: str
    order_status: str
    total_price: float
    order_date: Optional[datetime] = None
    order_details: List[OrderDetail] = []

    class ConfigDict:
        from_attributes = True

class OrderUpdate(BaseModel):
    order_status: Optional[str] = None
    tracking_number: Optional[str] = None
    promotion_id: Optional[int] = None
    order_type: Optional[str] = None