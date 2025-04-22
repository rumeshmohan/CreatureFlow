from pydantic import BaseModel
from typing import Optional

class Pokemon(BaseModel):
    id: int
    name: str
    species: Optional[str] = None
    power: int

    model_config = {"from_attributes": True}

class Character(BaseModel):
    id: int
    name: str
    status: Optional[str]  = None
    species: Optional[str] = None

    model_config = {"from_attributes": True}
