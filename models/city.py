#!/usr/bin/python3
"""City class"""

from models.base_model import BaseModel


class City(BaseModel):
    """City class definition

    Attributes:
        state_id (str): state id of the city
        name (str): name of the city

    """

    state_id = ""
    name = ""
