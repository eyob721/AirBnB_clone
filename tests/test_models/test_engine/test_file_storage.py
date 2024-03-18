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
