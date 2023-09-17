#!/usr/bin/python3
"""  class Amenity that inherits from BaseModel:"""
from models.base_model import BaseModel, Base
from sqlalchemy import *
from models.place import place_amenity
from sqlalchemy.orm import *


class Amenity(BaseModel, Base):
    """Public class attributes
    name: string - empty string"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary=place_amenity)
