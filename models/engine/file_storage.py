#!/usr/bin/python3
"""FileStorage

This module contains the FileStorage class definition, which is used to
serialize instances to a JSON file and deserialize JSON file to instances

"""
import json

from models.base_model import BaseModel


class FileStorage:
    """FileStorage class definition"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to json file"""
        obj_dict = {
            key: obj.to_dict() for key, obj in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, "w") as file:
            json.dump(obj_dict, file, indent=4)
            file.write("\n")

    def reload(self):
        """Deserializes the json file to __objects"""
        try:
            with open(FileStorage.__file_path, "r") as file:
                # TODO: handle empty file
                obj_dict = json.load(file)
        except FileNotFoundError:
            pass
        else:
            FileStorage.__objects = {
                key: eval("{}(**{})".format(o_dict["__class__"], o_dict))
                for key, o_dict in obj_dict.items()
            }
