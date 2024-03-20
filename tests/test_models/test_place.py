#!/usr/bin/python3
"""Tests for the Place class"""
from unittest import TestCase

from models.base_model import BaseModel
from models.place import Place


class TestPlaceClass(TestCase):
    """Tests for the Place class"""

    def test_instance_type(self):
        """Check that Place instance type and inheritance"""
        p = Place()
        self.assertTrue(type(p) is Place)
        self.assertTrue(
            type(p) is not BaseModel and issubclass(type(p), BaseModel)
        )

    def test_attributes_type_and_value(self):
        """Check that the right attributes for Place are defined correctly"""
        valid_str_attrs = ["city_id", "user_id", "name", "description"]
        valid_int_attrs = [
            "number_rooms",
            "number_bathrooms",
            "max_guest",
            "price_by_night",
        ]
        valid_float_attrs = ["latitude", "longitude"]

        p = Place()

        for str_attr in valid_str_attrs:
            value = getattr(Place, str_attr)
            self.assertIn(str_attr, dir(p))
            self.assertIs(type(value), str)
            self.assertEqual(value, "")

        for int_attr in valid_int_attrs:
            value = getattr(Place, int_attr)
            self.assertIn(int_attr, dir(p))
            self.assertIs(type(value), int)
            self.assertEqual(value, 0)

        for float_attr in valid_float_attrs:
            value = getattr(Place, float_attr)
            self.assertIn(float_attr, dir(p))
            self.assertIs(type(value), float)
            self.assertEqual(value, 0.0)

        # Check for the only valid list attribute
        value = getattr(Place, "amenity_ids")
        self.assertIn("amenity_ids", dir(p))
        self.assertIs(type(value), list)
        self.assertEqual(value, [])
