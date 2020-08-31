from typing import Type

from nanoid import generate
from peewee import ForeignKeyField, CharField

from .base_models import AudioModel, BaseModel
from .project_model import Project


class AudioGrab(AudioModel):
    project = ForeignKeyField(Project, backref='audio_grabs')
    lang = CharField(null=True)


class Music(AudioModel):
    project = ForeignKeyField(Project, backref='music')


class Mix(AudioGrab):
    project = ForeignKeyField(Project, backref='mixes')
    lang = CharField(null=True)


class Stem(AudioModel):
    project = ForeignKeyField(Project, backref='stems')
    lang = CharField(null=True)


class WorkingAudio(BaseModel):
    name = CharField()
    location = CharField()
    link = CharField(null=True)
    project = ForeignKeyField(Project, backref='int_audio')
    music = ForeignKeyField(Music, backref='int_music', null=True)
    mix = ForeignKeyField(Mix, backref='int_mix', null=True)
    stem = ForeignKeyField(Stem, backref='int_stems', null=True)

    # def upsert(self, project:Type[Project], name:str, loc:str, **kwargs)
    #     if 'music' in **kwargs:
    #         integrated = (self
    #             .replace(project = project, **{})
    #         )
    #     elif 'mix' in **kwargs:

    #     elif 'stem' in **kwargs:
            
    #     else:
    #         return None