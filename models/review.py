#!/usr/bin/python3
"""Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Review class definition

    Attributes:
        place_id (str): place id
        user_id (str): user id
        text (str): review text

    """

    place_id = ""
    user_id = ""
    text = ""
