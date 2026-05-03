from typing import Optional, List
from pydantic import BaseModel
from .resources import Resource

class RecipeBase(BaseModel):
    menu_item_id: int
    resource_id: int
    quantity_required: float

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    menu_item_id: Optional[int] = None
    resource_id: Optional[int] = None
    quantity_required: Optional[float] = None

class Recipe(RecipeBase):
    resource: Resource = None

    class ConfigDict:
        from_attributes = True