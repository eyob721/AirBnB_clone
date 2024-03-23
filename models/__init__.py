#!/usr/bin/python3
"""Initialises the file storage for the console"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
