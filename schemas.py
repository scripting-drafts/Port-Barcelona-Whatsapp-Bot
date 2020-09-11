from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class Incident(BaseModel):
    id:str
    inc_type:str
    inc_detail:str
    lat:float
    lon:float
    url:str
    pic:str
    timestamp:datetime = datetime.now()
    
class Item(Incident):
    id: str
    owner_id: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: str

class User(UserBase):
    id: str
    items: List[Item] = []

    class Config:
        orm_mode = True
