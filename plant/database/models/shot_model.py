from typing import Type

from nanoid import generate
from peewee import ForeignKeyField, CharField, IntegerField, FloatField
from retrying import retry

from .base_models import BaseModel
from .project_model import Project

class Shot(BaseModel):
    project = ForeignKeyField(Project, backref='shots')
    name = CharField(null=True)
    shot = IntegerField()
    sequence = IntegerField(null=True)
    duration = IntegerField(null=True)
    framerate = FloatField(null=True)

    @retry(wait_random_min=250, wait_random_max=2000, stop_max_attempt_number=10)
    def new_or_get(self, project:Type[Project], name:str, shot:int, **kwargs):
        new_shot, _ = self.get_or_create(
            project = project,
            name = name,
            shot = shot,
            defaults = {'guid': generate(), **kwargs}
        )
        return new_shot