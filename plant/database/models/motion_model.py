from typing import Type

from nanoid import generate
from peewee import ForeignKeyField
from retrying import retry

from .base_models import VisModel
from .shot_model import Shot

class Motion(VisModel):
    shot = ForeignKeyField(Shot, backref='motion')

    @retry(
        wait_random_min=250, 
        wait_random_max=2000, 
        stop_max_attempt_number=10
    )
    def new_or_get(
        self,
        shot:Type[Shot],
        name: str,
        location:str,
        **kwargs
    ):
        new_motion_shot, _ = self.get_or_create(
            shot = shot,
            name = name,
            defaults = {
                'guid': generate(),
                'location': location,
                **kwargs,
            }
        )
        return new_motion_shot
