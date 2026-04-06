from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promotion_code = Column(String(50), unique=True, index=True, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    discount_percentage = Column(Float, nullable=False)

    orders = relationship("Order", back_populates="promotion")