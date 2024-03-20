#!/user/bin/python3
"""we implement review class that inherites from BaseModel"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Class definition of the Review class"""

    place_id = ""
    user_id = ""
    text = ""
