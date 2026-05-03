from pydantic import BaseModel

class RevenueResponse(BaseModel):
    total_orders: int
    total_revenue: float