#!/usr/bin/python3
"""Tests for the City class"""
from unittest import TestCase

from models.base_model import BaseModel
from models.city import City


class TestCityClass(TestCase):
    """Tests for the City class"""

    def test_instance_type(self):
        """Check that City instance type and inheritance"""
        c = City()
        self.assertTrue(type(c) is City)
        self.assertTrue(
            type(c) is not BaseModel and issubclass(type(c), BaseModel)
        )

    def test_attributes_type_and_value(self):
        """Check that the right attributes for City are defined correctly"""
        valid_attrs = ["state_id", "name"]

        c = City()
        for attr in valid_attrs:
            value = getattr(City, attr)
            self.assertIn(attr, dir(c))
            self.assertIs(type(value), str)
            self.assertEqual(value, "")
