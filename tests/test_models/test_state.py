#!/usr/bin/python3
"""Tests for the State class"""
from unittest import TestCase

from models.base_model import BaseModel
from models.state import State


class TestStateClass(TestCase):
    """Tests for the State class"""

    def test_instance_type(self):
        """Check that State instance type and inheritance"""
        s = State()
        self.assertTrue(type(s) is State)
        self.assertTrue(
            type(s) is not BaseModel and issubclass(type(s), BaseModel)
        )

    def test_attributes_type_and_value(self):
        """Check that the right attributes for State are defined correctly"""
        s = State()
        self.assertIn("name", dir(s))

        value = getattr(State, "name")
        self.assertIs(type(value), str)
        self.assertEqual(value, "")
