from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class IncType(str, Enum):
    vertido = "vertido"
    objeto = "objeto"
    animales = "animales"
    olores = "olores"
    ruido = "ruido"
    polvo = "polvo"
    humo = "humo"
    otros = "otros"

class IncDetail(str, Enum):
    mar = "mar"
    darsena = "dársena"
    calzada = "calzada"
    flotante = "flotante"
    aves = "aves muertas"
    malolor = "mal olor"
    olorquimico = "olor químico"
    puerto = "puerto"
    embarcacion = "embarcación"
    soja = "soja"
    otros = "otros"


class Incident(BaseModel):
    id:int
    inc_type:IncType
    inc_detail:IncDetail
    lat:float
    lon:float
    timestamp:datetime = datetime.now()
    is_active:bool


class ItemCreate(Incident):
    pass


class Item(Incident):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
