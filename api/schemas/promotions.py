from pydantic import BaseModel
from datetime import datetime

class PromotionBase(BaseModel):
    promotion_code: str
    expiration_date: datetime
    discount_percentage: float

class PromotionCreate(PromotionBase):
    pass

class Promotion(PromotionBase):
    id: int

    class Config:
        orm_mode = True