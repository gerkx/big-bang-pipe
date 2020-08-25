import datetime

# from nanoid import generate
from peewee import (
    Model, CharField, DateTimeField, UUIDField, IntegerField, ForeignKeyField, 
    SqliteDatabase, FloatField
)


db = SqliteDatabase('temp.db')

class BaseModel(Model):
    guid = UUIDField()
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.date.now, null=True)
    
    class Meta:
        database = db

class User(Model):
    guid = UUIDField()
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    asana_id = CharField(null=True, unique=True)
    skype = CharField(null=True)
    phone = CharField(null=True)
    shotgun = CharField(null=True)

    class Meta:
        database = db

class Client(BaseModel):
    name = CharField()

class Project(BaseModel):
    client = ForeignKeyField(Client, backref='projects')
    name = CharField()
    production_number:int = IntegerField(null=True)
    emission_number:int = IntegerField(null=True)

class Shot(BaseModel):
    project = ForeignKeyField(Project, backref='shots')
    name = CharField(null=True)
    shot = IntegerField()
    sequence = IntegerField(null=True)
    duration = IntegerField(null=True)
    framerate = FloatField(null=True)

class Render_Seq(BaseModel):
    shot = ForeignKeyField(Shot, backref='renders')
    location = CharField()
    name = CharField()
    inbound_name = CharField()
    duration = IntegerField(null=True)
    frames = CharField(null=True)
    transcode_name = CharField(null=True)
    transcode_location = CharField(null=True)
    transcode_link = CharField(null=True)
    mp4_name = CharField(null=True)
    mp4_location = CharField(null=True)
    mp4_link = CharField(null=True)









    



