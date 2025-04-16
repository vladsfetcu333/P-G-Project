from pydantic import BaseModel, ConfigDict
from typing import Optional

class PlantCreate(BaseModel):
    name: str
    location: str
    capacity: int

class PlantRead(PlantCreate):
    id: int
    name: str
    location: str
    capacity: int
    model_config = ConfigDict(from_attributes=True)

class PlantUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None