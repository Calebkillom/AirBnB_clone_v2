#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.review import Review
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity, place_amenity
import models


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"

    if getenv('HBNB_TYPE_STORAGE') == "db":
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship('Amenity', secondary=place_amenity,
                                 back_populates='place_amenities',
                                 viewonly=False)
        amenity_ids = []
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    @property
    def reviews(self):
        """
        Getter attribute to return the list of Review instances
        with place_id equals to the current Place.id
        """
        review_list = []

        for review in models.storage.all(Review).values():
            if review.place_id == self.id:
                review_list.append(review)

        return review_list

    @property
    def amenities(self):
        """
        returns the list of Amenity instances
        based on the attribute amenity_ids
        """
        amenity_list = []
        for amenity_id in self.amenity_ids:
            amenity = models.storage.get(Amenity, amenity_id)
            if amenity is not None:
                amenity_list.append(amenity)
        return amenity_list

    @amenities.setter
    def amenities(self, value):
        """
        amenities that handles append method
        for adding an Amenity.id to the attribute amenity_ids
        """
        if type(value) == Amenity:
                self.amenity_ids.append(value.id)
