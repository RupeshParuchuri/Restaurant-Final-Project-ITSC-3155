from sqlalchemy import Column, ForeignKey, Integer, String, Float, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=True)
    order_date = Column(DATETIME, server_default=str(datetime.now()))
    tracking_number = Column(String(100), unique=True, index=True)
    order_status = Column(String(50), server_default="Pending")
    total_price = Column(Float)

    customer = relationship("Customer", back_populates="orders")
    promotion = relationship("Promotion", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    payment = relationship("Payment", back_populates="order")