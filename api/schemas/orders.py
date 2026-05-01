from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail

class OrderBase(BaseModel):
    customer_id: Optional[int] = None #Optional for guest checkout
    promotion_id: Optional[int] = None
    customer_name: Optional[str] = None
    description: Optional[str] = None
    tracking_number: Optional[str] = None
    order_status: str = "Pending"
    total_price: Optional[float] = None
    order_type: str = "Takeout" #Takeout or Delivery

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    promotion_id: Optional[int] = None
    customer_name: Optional[str] = None
    description: Optional[str] = None
    tracking_number: Optional[str] = None
    order_status: Optional[str] = None
    total_price: Optional[float] = None
    order_type: Optional[str] = None

class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True