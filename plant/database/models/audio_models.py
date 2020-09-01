from typing import Type
from datetime import datetime

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
    grab = ForeignKeyField(AudioGrab, backref='int_grab', null=True)
    music = ForeignKeyField(Music, backref='int_music', null=True)
    mix = ForeignKeyField(Mix, backref='int_mix', null=True)
    stem = ForeignKeyField(Stem, backref='int_stems', null=True)

    def new_or_get(self,
        name:str,
        location:str,
        project:Type[Project],
        **kwargs
    ):
        working_audio, created = self.get_or_create(
            project = project,
            name = name,
            defaults = {
                'guid': generate(),
                'location': location,
                **kwargs
            } 
        )
        if not created:
            working_audio.update(location = location, modified = datetime.now(), **kwargs)
            working_audio.execute()
        return working_audio