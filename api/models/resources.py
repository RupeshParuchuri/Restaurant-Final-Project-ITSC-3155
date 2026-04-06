from sqlalchemy import Column, ForeignKey, Float, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    amount = Column(Float, index=True, nullable=False, server_default='0.0')
    unit = Column(String(50), nullable=False)

    recipes = relationship("Recipe", back_populates="resource")
