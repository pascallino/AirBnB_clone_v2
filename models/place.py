#!/usr/bin/python3
"""  class place that inherits from BaseModel:"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import *
from sqlalchemy.orm import *


class Place(BaseModel, Base):
    """place attributes for class Place"""
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenity_ids = []

    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            """getter attribute reviewa that returns the list
              of reviews instances with place_id equals to the
              current place.id"""
            reviewslist = []
            for rev in models.storage.all('Review').values():
                if rev.place_id == Place.id:
                    reviewslist.append(rev)
            return reviewslist
