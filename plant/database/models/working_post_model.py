from typing import Type
from datetime import datetime

from peewee import CharField, ForeignKeyField, IntegerField
from nanoid import generate
from retrying import retry

from .base_models import BaseModel
from .shot_model import Shot
from .render_model import Render
from .grade_model import Grade
from .compo_model import Compo
from .motion_model import Motion

class WorkingPost(BaseModel):
    shot = ForeignKeyField(Shot, backref='working_post', unique=True)
    name = CharField()
    location = CharField()
    link = CharField(null=True)
    render = ForeignKeyField(Render, backref='working_renders', null=True)
    grade = ForeignKeyField(Grade, backref='working_grades', null=True)
    compo = ForeignKeyField(Compo, backref='working_compos', null=True)
    motion = ForeignKeyField(Motion, backref='working_motion', null=True)

    @retry(wait_random_min=250, wait_random_max=2000, stop_max_attempt_number=10)
    def new_or_get(self,
        shot:Type[Shot],
        name:str,
        location:str,
        **kwargs
    ):
        working, created = self.get_or_create(
            shot = shot,
            defaults = {
                'guid': generate(),
                'location': location,
                'name': name,
                **kwargs
            }
        )

        if not created:
            u = (self
                .update(location = location, modified = datetime.now(), **kwargs)
                .where(self.guid == working.guid))
            u.execute()
        return working

