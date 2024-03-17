#!/usr/bin/python3
"""BaseModel

This module contains the class definition of the BaseModel class, which is
the parent class of all other classes that are used for the AirBnB console.

"""
import uuid
from datetime import datetime

import models


class BaseModel:
    """BaseModel class definition"""

    def __init__(self, *args, **kwargs):
        """BaseModel class constructor"""
        if kwargs:
            for key in kwargs:
                if key in ["created_at", "updated_at"]:
                    setattr(self, key, datetime.fromisoformat(kwargs[key]))
                    continue
                if key != "__class__":  # class name shouldn't be changed
                    setattr(self, key, kwargs[key])
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """String representation of the instance"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Saves the instance"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns dictionary representation of the instance"""
        obj_dict = {"__class__": type(self).__name__}
        for attr in self.__dict__:
            if attr in ["created_at", "updated_at"]:
                obj_dict[attr] = self.__dict__[attr].isoformat()
                continue
            obj_dict[attr] = self.__dict__[attr]
        return obj_dict
