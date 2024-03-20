#!/usr/bin/python3
"""Tests for the User class"""
from unittest import TestCase

from models.base_model import BaseModel
from models.user import User


class TestUserClass(TestCase):
    """Tests for the User class"""

    def test_instance_type(self):
        """Check that User instance type and inheritance"""
        u = User()
        self.assertTrue(type(u) is User)
        self.assertTrue(
            type(u) is not BaseModel and issubclass(type(u), BaseModel)
        )

    def test_attributes_type_and_value(self):
        """Check that the right attributes for User are defined correctly"""
        valid_attrs = ["email", "password", "first_name", "last_name"]

        u = User()
        for attr in valid_attrs:
            value = getattr(User, attr)
            self.assertIn(attr, dir(u))
            self.assertIs(type(value), str)
            self.assertEqual(value, "")
