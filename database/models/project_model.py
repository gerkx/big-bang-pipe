from peewee import CharField, ForeignKeyField, IntegerField

from .base_models import BaseModel
from .client_model import Client

class Project(BaseModel):
    client = ForeignKeyField(Client, backref='projects')
    name = CharField()
    production_number:int = IntegerField(null=True)
    emission_number:int = IntegerField(null=True)