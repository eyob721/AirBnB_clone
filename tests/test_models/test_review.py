#!/usr/bin/python3
"""Tests for the Review class"""
from unittest import TestCase

from models.base_model import BaseModel
from models.review import Review


class TestReviewClass(TestCase):
    """Tests for the Review class"""

    def test_instance_type(self):
        """Check that Review instance type and inheritance"""
        r = Review()
        self.assertTrue(type(r) is Review)
        self.assertTrue(
            type(r) is not BaseModel and issubclass(type(r), BaseModel)
        )

    def test_attributes_type_and_value(self):
        """Check that the right attributes for Review are defined correctly"""
        valid_attrs = ["place_id", "user_id", "text"]

        r = Review()
        for attr in valid_attrs:
            value = getattr(Review, attr)
            self.assertIn(attr, dir(r))
            self.assertIs(type(value), str)
            self.assertEqual(value, "")
