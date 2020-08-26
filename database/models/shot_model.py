from typing import Type

from nanoid import generate
from peewee import ForeignKeyField, CharField, IntegerField, FloatField

from .base_models import BaseModel
from .project_model import Project

class Shot(BaseModel):
    project = ForeignKeyField(Project, backref='shots')
    name = CharField(null=True)
    shot = IntegerField()
    sequence = IntegerField(null=True)
    duration = IntegerField(null=True)
    framerate = FloatField(null=True)

    def new_or_get(self, project:Type[Project], name:str, shot:int, **kwargs):
        new_shot, _ = self.get_or_create(
            project = project,
            name = name,
            defaults = {'guid': generate(), **kwargs}
        )
        return new_shot