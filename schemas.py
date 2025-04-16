from pydantic import BaseModel
from typing import Optional
class PlantCreate(BaseModel):
    name: str
    location: str
    capacity: int

class PlantRead(PlantCreate):
    id: int

    class Config:
        orm_mode = True
        
class PlantUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None