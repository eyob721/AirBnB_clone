#!/usr/bin/python3
"""BaseModel"""
import uuid
from datetime import datetime

class BaseModel:
    """BaseModel class definition"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        obj_dict = {"__class__": type(self).__name__}
        for attr in self.__dict__:
            if attr in ["created_at", "updated_at"]:
                obj_dict[attr] = self.__dict__[attr].isoforamt()
                continue
            obj_dict[attr] = self.__dict__[attr]
        return obj_dict
        