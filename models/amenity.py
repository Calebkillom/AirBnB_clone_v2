#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True, nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True, nullable=False))


class Amenity(BaseModel, Base):
    """ Amenity Class Implementation """

    __tablename__ = "amenities"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary=place_amenity)
    else:
        name = ""
