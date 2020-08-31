from typing import Type

from nanoid import generate
from peewee import ForeignKeyField, CharField

from .base_models import VisModel
from .shot_model import Shot

class Compo(VisModel):
    shot = ForeignKeyField(Shot, backref='compo')

    def new_or_get(
        self, 
        shot:Type[Shot], 
        name:str, 
        location:str, 
        inbound_name:str, 
        **kwargs
    ):
        new_compo_shot, _ = self.get_or_create(
            shot = shot,
            name = name,
            defaults = {
                'guid': generate(),
                'inbound_name': inbound_name,
                'location': location 
                **kwargs
            }
        )
        return new_compo_shot