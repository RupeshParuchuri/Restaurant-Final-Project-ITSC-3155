from pydantic import BaseModel

class OrderDetailBase(BaseModel):
    menu_item_id: int
    amount: int

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetail(OrderDetailBase):
    id: int
    order_id: int

    class ConfigDict:
        from_attributes = True