from pydantic import BaseModel, Field
from typing import Optional

class ReviewBase(BaseModel):
    customer_id: int
    menu_item_id: int
    review_text: Optional[str] = None
    score: int = Field(..., ge=1, le=5)

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class Config:
        from_attributes = True