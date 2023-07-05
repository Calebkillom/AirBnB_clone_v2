#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initializing the default attributes
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()

        """
        Updating the attributes with provided kwargs
        """
        for key, value in kwargs.items():
            if key == "created_at" or key == "updated_at":
                value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            if key != "__class__":
                setattr(self, key, value)

        """
        Updating the attributes if not provided in kwargs
        """
        if 'id' not in kwargs:
            self.id = str(uuid.uuid4())
        if 'created_at' not in kwargs:
            self.created_at = datetime.now()
        if 'updated_at' not in kwargs:
            self.updated_at = self.created_at

    def __str__(self):
        """Returns a string representation of the BaseModel Class"""
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Return dictionary representation of BaseModel class.
        """
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__

        if 'updated_at' in dictionary:
            dictionary['updated_at'] = dictionary['updated_at'].strftime(
                "%Y-%m-%dT%H:%M:%S.%f")
        if 'created_at' in dictionary:
            dictionary['created_at'] = dictionary['created_at'].strftime(
                "%Y-%m-%dT%H:%M:%S.%f")

        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def delete(self):
        """
        Delete the current instance from the storage.
        """
        models.storage.delete(self)
