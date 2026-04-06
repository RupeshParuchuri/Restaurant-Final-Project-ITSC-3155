from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    customer_id: int
    menu_item_id: int
    review_text: Optional[str] = None
    score: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True