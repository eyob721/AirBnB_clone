#!/usr/bin/python3
"""Place class"""
from models.base_model import BaseModel


class Place(BaseModel):
    """Place class definition

    Attributes:
        city_id (str): city id
        user_id (str): user id
        name (str): name of the place
        description (str): description about the place
        number_rooms (int): number of rooms
        number_bathrooms (int): number of bathrooms
        max_guest (int): max number of guest allowed
        price_by_night (int): price per night
        latitude (float): latitude place location
        longitude (float): longitude place location

    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
