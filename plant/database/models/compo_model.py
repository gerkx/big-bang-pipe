from typing import Type

from nanoid import generate
from peewee import ForeignKeyField, CharField
from retrying import retry

from .base_models import VisModel
from .shot_model import Shot

class Compo(VisModel):
    shot = ForeignKeyField(Shot, backref='compo')

    @retry(wait_random_min=250, wait_random_max=2000, stop_max_attempt_number=10)
    def new_or_get(
        self, 
        shot:Type[Shot], 
        name:str, 
        location:str, 
        inbound_name:str, 
        **kwargs
    ):
        print(f'location: {location}')
        new_compo_shot, _ = self.get_or_create(
            shot = shot,
            name = name,
            defaults = {
                'guid': generate(),
                'inbound_name': inbound_name,
                'location': location, 
                **kwargs
            }
        )
        return new_compo_shot