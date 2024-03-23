#!/usr/bin/python3
"""FileStorage

This module contains the FileStorage class definition, which is used to
serialize instances to a JSON file and deserialize JSON file to instances

"""
import json

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """This class saves and manages the data using a JSON file"""

    __file_path = "hbnb.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Add `obj` to the dictionary of objects with key <class name>.id"""
        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes the dictionary of objects to a JSON file"""
        obj_dict = {
            key: obj.to_dict() for key, obj in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, "w") as file:
            json.dump(obj_dict, file, indent=4)
            file.write("\n")

    def reload(self):
        """Deserializes the JSON file to a dictionary of objects"""
        try:
            with open(FileStorage.__file_path, "r") as file:
                obj_dict = json.load(file)
        except FileNotFoundError:
            pass
        else:
            FileStorage.__objects = {
                key: eval("{}(**{})".format(o_dict["__class__"], o_dict))
                for key, o_dict in obj_dict.items()
            }
