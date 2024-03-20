#!/usr/bin/python3
"""Unit tests for the FileStorage class"""
import json
import os
from datetime import datetime, timedelta
from unittest import TestCase
from uuid import uuid4

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


def remove_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)


valid_classes = (
    "Amenity",
    "BaseModel",
    "City",
    "Place",
    "Review",
    "State",
    "User",
)


class TestFileStorageClass(TestCase):
    """Tests for the FileStorage class (general)"""

    def test_instance_type(self):
        """Check instance of FileStorage is instance of FileStorage"""
        f = FileStorage()
        self.assertIs(type(f), FileStorage)


class TestFileStorageAttributes(TestCase):
    """Tests for the attributes of FileStorage class"""

    def test_attributes_exist(self):
        """Check that the right attributes exist"""
        valid_attrs = ["_FileStorage__file_path", "_FileStorage__objects"]

        for attr in valid_attrs:
            self.assertTrue(attr in dir(FileStorage))

    def test__file_path(self):
        """Check the __file_path type and value"""
        __file_path = getattr(FileStorage, "_FileStorage__file_path")

        # Check that __file_path is a str
        self.assertIs(type(__file_path), str)

        # Check the __file_path value
        self.assertRegex(__file_path, r"^.+\.json$")

    def test__objects(self):
        """Check the __objects type and content"""
        __objects = getattr(FileStorage, "_FileStorage__objects")

        # Check that __objects is a dict
        self.assertIs(type(__objects), dict)

        # Check the contents of the __objects dictionary
        for key in __objects:
            # Check key pattern
            # NOTE: use valid classes, ({}) -> (BaseModel|User|...)
            pattern = r"^({})+\.\w+-\w+-\w+-\w+-\w+$".format(
                "|".join(valid_classes)
            )
            self.assertRegex(key, pattern)
            # Check object
            obj = __objects[key]
            self.assertIsInstance(obj, BaseModel)


class TestFileStorageMethods(TestCase):
    """Tests for the methods of FileStorage class"""

    def test_methods_exist(self):
        """Check that the right methods exist"""
        valid_methods = ["all", "new", "save", "reload"]
        for method in valid_methods:
            self.assertTrue(method in dir(FileStorage))

    def test_save_and_reload(self):
        """Check that the save and reload methods work correctly"""
        f = FileStorage()
        __file_path = getattr(f, "_FileStorage__file_path")

        f.save()
        __objects = getattr(f, "_FileStorage__objects")
        obj_dict_before = {
            key: obj.to_dict() for key, obj in __objects.items()
        }

        # Check that the file is created
        if not os.path.exists(__file_path):
            raise AssertionError("JSON file not found")

        f.reload()
        __objects = getattr(f, "_FileStorage__objects")
        obj_dict_after = {key: obj.to_dict() for key, obj in __objects.items()}

        # Check what got out is the same as what got in
        self.assertEqual(obj_dict_before, obj_dict_after)

    def test_all_method(self):
        """Check return type and value of the all method"""
        f = FileStorage()

        # check return type
        self.assertIs(type(f.all()), dict)

        # check return value
        __objects = getattr(f, "_FileStorage__objects")
        self.assertIs(__objects, f.all())

    def test_new_method(self):
        """Check that the new method works correctly"""
        for cls in valid_classes:
            id = str(uuid4())
            obj = eval("{}(**{})".format(cls, {"id": id, "Alx": "is awesome"}))
            f = FileStorage()
            f.new(obj)

            key = f"{type(obj).__name__}.{id}"
            __objects = getattr(f, "_FileStorage__objects")

            self.assertIn(key, __objects.keys())
            self.assertIs(__objects[key], obj)


class TestFileStorageLinkToBaseModel(TestCase):
    """Test FileStorage link to BaseModel"""

    def test_new_instances_are_add_to__objects(self):
        """Check that new instances are added to the __objects dictionary"""
        for cls in valid_classes:
            obj = eval("{}()".format(cls))

            key = f"{cls}.{obj.id}"
            __objects = getattr(FileStorage, "_FileStorage__objects")

            self.assertIn(key, __objects.keys())
            self.assertIs(__objects[key], obj)

    def test_save_method_from_BaseModel_object(self):
        """Check calling the save method from a BaseModel object"""
        b = BaseModel()
        __file_path = getattr(FileStorage, "_FileStorage__file_path")

        b.save()
        __objects = getattr(FileStorage, "_FileStorage__objects")
        obj_dict_before = {
            key: obj.to_dict() for key, obj in __objects.items()
        }

        FileStorage().reload()
        __objects = getattr(FileStorage, "_FileStorage__objects")
        obj_dict_after = {key: obj.to_dict() for key, obj in __objects.items()}

        # Check what got out is the same as what got in
        self.assertEqual(obj_dict_before, obj_dict_after)
