from typing import Optional
from pydantic import BaseModel

class ResourceBase(BaseModel):
    name: str
    amount: float

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None

class Resource(ResourceBase):
    id: int

    class ConfigDict:
        from_attributes = True