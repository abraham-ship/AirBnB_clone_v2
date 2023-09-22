#!/usr/bin/python3
"""Class db_storage"""
from models.base_model import BaseModel, Base
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """New engine"""
    __engine = None
    __session = None

    def __init__(self):
        """initialization of class"""

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on current db of all objects depending on name"""
        objects = {}
        classes = [State, City, User, Place, Review, Amenity]
        if cls:
            if cls in classes:
                query_result = self.__session.query(cls).all()
                for obj in query_result:
                    key = f'{cls.__name__}.{obj.id}'
                    objects[key] = obj
        else:
            for cls in classes:
                query_result = self.__session.query(cls).all()
                for obj in query_result:
                    key = f'{cls.__name__}.{obj.id}'
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.close()
