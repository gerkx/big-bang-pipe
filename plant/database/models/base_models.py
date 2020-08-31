import datetime
from typing import Type

from peewee import (
    Model, SqliteDatabase, AutoField, UUIDField, 
    DateTimeField, CharField, IntegerField
)
from nanoid import generate

from .project_model import Project

db = SqliteDatabase('temp.db')

class BaseModel(Model):
    id = AutoField()
    guid = CharField()
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now, null=True)
    
    class Meta:
        database = db

class VisModel(BaseModel):
    location = CharField()
    name = CharField()
    inbound_name = CharField()
    duration = IntegerField(null=True)
    frames = CharField(null=True)

class AudioModel(BaseModel):
    name = CharField()
    inbound_name = CharField()
    location = CharField()
    mp3_name = CharField(null=True)
    mp3_location = CharField(null=True)
    mp3_link = CharField(null=True)

    def new_or_get(self,
        project:Type[Project],
        name:str,
        inbound_name: str,
        location:str,
        **kwargs
    ):
        audio, _ = self.get_or_create(
            project = project,
            name = name,
            defaults = {
                'guid': generate(),
                'inbound_name': inbound_name,
                'location': location,
                **kwargs
            }
        )
        return audio