#!/usr/bin/python3
"""Tests for the Amenity class"""
from unittest import TestCase

from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenityClass(TestCase):
    """Tests for the Amenity class"""

    def test_instance_type(self):
        """Check that Amenity instance type and inheritance"""
        a = Amenity()
        self.assertTrue(type(a) is Amenity)
        self.assertTrue(
            type(a) is not BaseModel and issubclass(type(a), BaseModel)
        )

    def test_attributes_type_and_value(self):
        """Check that the right attributes for Amenity are defined correctly"""
        a = Amenity()
        self.assertIn("name", dir(a))

        value = getattr(Amenity, "name")
        self.assertIs(type(value), str)
        self.assertEqual(value, "")
