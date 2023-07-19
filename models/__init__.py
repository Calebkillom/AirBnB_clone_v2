#!/usr/bin/python3
""" instantiates an object of the classes FileStorage and DBStorage """
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
classes = {"User": User, "BaseModel": BaseModel,
           "State": State, "City": City}
storage.reload()
