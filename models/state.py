#!/user/bin/python3
"""we implement state class that inherites from BaseModel"""
import cmd
from models.base_model import BaseModel

class state(BaseModel):
    """"Class definition of state class"""
    
    name = ""