#!/usr/bin/python3
""" New engine DBStorage """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.user import User
from models.city import City


class DBStorage:
    """ DBStorage Storage """
    __engine = None
    __session = None

    def __init__(self):
        """ creating the engine and linking to the MYSQL database """
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        database = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(user, password, host, database),
                                      pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

        Base.metadata.create_all(self.__engine)

        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def all(self, cls=None):
        """
        querying on the current database session
        on all objects depending of the class name
        querying all types of objects
        returning a dictionary
        """
        from models import classes
        objects = {}
        if cls:
            query = self.__session.query(classes[cls]).all()
        else:
            query = []
            for cls in classes.values():
                query += self.__session.query(cls).all()

        for obj in query:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            objects[key] = obj

        return objects

    def new(self, obj):
        """ adding the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ commiting all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ deleting from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        creating all tables in the database
        and creating the current database session
        from the engine
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)
