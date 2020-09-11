from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True)
    inc_type = Column(String, index=True)
    inc_detail = Column(String, index=True)
    lat = Column(Float, index=True)
    lon = Column(Float, index=True)
    url = Column(String, index=True)
    pic = Column(String, index=True)
    timestamp = Column(String, index=True)
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
