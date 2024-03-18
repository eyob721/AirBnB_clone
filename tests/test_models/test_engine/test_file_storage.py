#!/usr/bin/python3
"""Unit tests for the FileStorage class"""
import json
import os
from datetime import datetime, timedelta
from unittest import TestCase

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
        f = FileStorage()
        valid_attrs = ["_FileStorage__file_path", "_FileStorage__objects"]

        for attr in valid_attrs:
            self.assertTrue(attr in dir(f))

    def test__file_path(self):
        f = FileStorage()
        __file_path = getattr(f, "_FileStorage__file_path")

        # Check that __file_path is a str
        self.assertIs(type(__file_path), str)

        # Check the __file_path value
        self.assertRegex(__file_path, r"^.+\.json$")

    def test__objects(self):
        f = FileStorage()
        __objects = getattr(f, "_FileStorage__objects")

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
