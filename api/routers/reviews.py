from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..dependencies.database import get_db
from ..models.reviews import Review as ReviewModel
from ..schemas.reviews import ReviewCreate, Review

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

@router.post("/", response_model=Review)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    new_review = ReviewModel(**review.model_dump())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/", response_model=List[Review])
def get_reviews(
    menu_item_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(ReviewModel)

    if menu_item_id:
        query = query.filter(ReviewModel.menu_item_id == menu_item_id)

    reviews = query.all()

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")

    return reviews