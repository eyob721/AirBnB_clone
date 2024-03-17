#!/usr/bin/python3
"""Unit tests for the BaseModel class"""
from datetime import datetime, timedelta
from time import sleep
from unittest import TestCase

from models.base_model import BaseModel


class TestBaseModelClass(TestCase):
    """Tests for the BaseModel class"""

    def test_instance_type(self):
        b = BaseModel()
        self.assertTrue(type(b) is BaseModel)

    def test_instantiation_with_kwargs(self):
        b1 = BaseModel()
        b1.program = "Alx"  # pyright: ignore
        b1.cohort = 21  # pyright: ignore

        b2 = BaseModel(**b1.to_dict())

        self.assertEqual(b1.to_dict(), b2.to_dict())
        self.assertFalse(b1 is b2)


class TestBaseModelAttributes(TestCase):
    """Tests for the attributes of BaseModel"""

    def test_attributes_exist(self):
        valid_attr = ["id", "created_at", "updated_at"]
        b = BaseModel()
        for attr in valid_attr:
            self.assertTrue(attr in dir(b))

    def test_id_attribute(self):
        b = BaseModel()

        # Check type of id
        self.assertIs(type(b.id), str)

        # Check value of id
        self.assertRegex(b.id, r"^\w+-\w+-\w+-\w+-\w+$")

    def test_datetime_attributes_at_instantiation(self):
        current_time = datetime.now()
        b = BaseModel()

        # Check created_at attribute type
        self.assertIs(type(b.created_at), datetime)

        # Check created_at attribute value
        self.assertAlmostEqual(
            current_time,
            b.created_at,
            delta=timedelta(seconds=1),
            msg="created_at value is not the current datetime",
        )

        # Check updated_at attribute type
        self.assertIs(type(b.updated_at), datetime)

        # Check updated_at attribute value
        self.assertEqual(
            b.created_at,
            b.updated_at,
            msg="updated_at != created_at at instantiation",
        )


class TestBaseModelSaveMethod(TestCase):
    """Tests for the save method of BaseModel"""

    def test_save_method_is_defined(self):
        self.assertTrue(
            "save" in dir(BaseModel()), msg="save method is not defined"
        )

    def test_save_method_works_correctly(self):
        # Check that the updated_at attribute is updated upon save
        b = BaseModel()
        sleep(3)
        current_time = datetime.now()
        b.save()
        self.assertAlmostEqual(
            b.updated_at,
            current_time,
            delta=timedelta(seconds=1),
            msg="updated_at attributte is not updated with "
            + "current datetime upon save",
        )


class TestBaseModelTo_DictMethod(TestCase):
    """Tests for the to_dict method of BaseModel"""

    def test_to_dict_method_is_defined(self):
        self.assertTrue(
            "to_dict" in dir(BaseModel()), msg="to_dict method is not defined"
        )

    def test_to_dict_method_return_value(self):
        b = BaseModel()
        valid_keys = ["__class__", "id", "created_at", "updated_at"]
        b_dict = b.to_dict()

        # Check returned object is a dict
        self.assertIs(type(b_dict), dict)

        # Check valid_keys exist
        for key in valid_keys:
            self.assertTrue(key in b_dict)

        # Check type of value
        for key in b_dict:
            self.assertIs(type(b_dict[key]), str)

        # Check value of keys in the returned dict
        # __class__
        self.assertEqual(b_dict["__class__"], type(b).__name__)
        # id
        self.assertRegex(b_dict["id"], r"^\w+-\w+-\w+-\w+-\w+$")
        # created_at
        self.assertEqual(b_dict["created_at"], b.created_at.isoformat())
        # updated_at
        self.assertEqual(b_dict["updated_at"], b.updated_at.isoformat())
