#!/usr/bin/python3
"""User"""

from models.base_model import BaseModel


class User(BaseModel):
    """User class definition

    Attributes:
        email (str): email address of the user
        password (str): password of the user
        first_name (str): first name of the user
        last_name (str): last name of the user

    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
