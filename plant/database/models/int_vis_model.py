from typing import Type

from peewee import CharField, ForeignKeyField, IntegerField
from nanoid import generate

from .base_models import BaseModel
from .shot_model import Shot
from .render_seq_model import RenderSeq
from .grade_model import Grade
from .compo_model import Compo

class IntVis(BaseModel):
    shot = ForeignKeyField(Shot, backref='int_vis', unique=True)
    name = CharField()
    location = CharField()
    link = CharField(null=True)
    render = ForeignKeyField(RenderSeq, backref='int_renders', null=True)
    grade = ForeignKeyField(Grade, backref='int_grades', null=True)
    compo = ForeignKeyField(Compo, backref='int_compos', null=True)

    def upsert(self, shot:Type[Shot], name:str, loc:str, **kwargs):
        int_vis = (self
            .replace(shot = shot, **{'name': name, 'locaction': loc, **kwargs})
            .execute())
        return int_vis
                    
