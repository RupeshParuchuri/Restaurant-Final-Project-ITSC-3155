from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import reviews as model


def create(db: Session, request):
    if request.score < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Review score must be exactly between 1 and 5.")
    if request.score > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Review score must be exactly between 1 and 5.")

    new_item = model.Review(
        customer_id=request.customer_id,
        menu_item_id=request.menu_item_id,
        review_text=request.review_text,
        score=request.score
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def read_all(db: Session):
    result = db.query(model.Review).all()
    return result