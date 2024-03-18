#!/usr/bin/python3
"""Unit tests for the FileStorage class"""
import json
import os
from datetime import datetime, timedelta
from unittest import TestCase
from uuid import uuid4

from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


def remove_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)


class TestFileStorageClass(TestCase):
    """Tests for the FileStorage class (general)"""

    def test_instance_type(self):
        f = FileStorage()
        self.assertIs(type(f), FileStorage)


class TestFileStorageAttributes(TestCase):
    """Tests for the attributes of FileStorage class"""

    def test_attributes_exist(self):
        valid_attrs = ["_FileStorage__file_path", "_FileStorage__objects"]

        for attr in valid_attrs:
            self.assertTrue(attr in dir(FileStorage))

    def test__file_path(self):
        __file_path = getattr(FileStorage, "_FileStorage__file_path")

        # Check that __file_path is a str
        self.assertIs(type(__file_path), str)

        # Check the __file_path value
        self.assertRegex(__file_path, r"^.+\.json$")

    def test__objects(self):
        __objects = getattr(FileStorage, "_FileStorage__objects")

        # Check that __objects is a dict
        self.assertIs(type(__objects), dict)

        # Check the contents of the __objects dictionary
        for key in __objects:
            # Check key pattern
            # TODO: use actual class names e.g. (BaseModel|User)
            self.assertRegex(key, r"^[a-zA-Z]+\.\w+-\w+-\w+-\w+-\w+$")
            # Check object
            obj = __objects[key]
            self.assertIsInstance(obj, BaseModel)


class TestFileStorageMethods(TestCase):
    """Tests for the methods of FileStorage class"""

    def test_methods_exist(self):
        valid_methods = ["all", "new", "save", "reload"]
        for method in valid_methods:
            self.assertTrue(method in dir(FileStorage))

    def test_save_and_reload(self):
        f = FileStorage()
        __file_path = getattr(f, "_FileStorage__file_path")

        f.save()
        __objects = getattr(f, "_FileStorage__objects")
        obj_dict_before = {
            key: obj.to_dict() for key, obj in __objects.items()
        }

        # Check file is created
        if not os.path.exists(__file_path):
            raise AssertionError("JSON file not found")

        f.reload()
        __objects = getattr(f, "_FileStorage__objects")
        obj_dict_after = {key: obj.to_dict() for key, obj in __objects.items()}

        # Check what got out is the same as what got in
        self.assertEqual(obj_dict_before, obj_dict_after)

    def test_all_method(self):
        f = FileStorage()

        # check return type
        self.assertIs(type(f.all()), dict)

        # check return value
        __objects = getattr(f, "_FileStorage__objects")
        self.assertIs(__objects, f.all())

    def test_new_method(self):
        id = str(uuid4())
        b = BaseModel(**{"id": id, "Alx": "is awesome"})
        f = FileStorage()
        f.new(b)

        key = f"{type(b).__name__}.{id}"
        __objects = getattr(f, "_FileStorage__objects")

        self.assertIn(key, __objects.keys())
        self.assertIs(__objects[key], b)


class TestFileStorageLinkToBaseModel(TestCase):
    """Test FileStorage link to BaseModel"""

    def test_new_base_model_objects_are_add_to__objects(self):
        b = BaseModel()

        key = f"BaseModel.{b.id}"
        __objects = getattr(FileStorage, "_FileStorage__objects")

        self.assertIn(key, __objects.keys())
        self.assertIs(__objects[key], b)

    def test_save_method(self):
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