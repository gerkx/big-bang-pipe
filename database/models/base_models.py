import datetime

from peewee import (
    Model, SqliteDatabase, AutoField, UUIDField, 
    DateTimeField, CharField, IntegerField
)

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