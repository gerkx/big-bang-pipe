from typing import Type

from peewee import CharField, ForeignKeyField, IntegerField
from nanoid import generate
from retrying import retry

from .base_models import BaseModel
from .client_model import Client

class Project(BaseModel):
    client = ForeignKeyField(Client, backref='projects')
    name = CharField(unique=True, null=True)
    production_number:int = IntegerField()
    emission_number:int = IntegerField(null=True)

    @retry(wait_random_min=250, wait_random_max=2000, stop_max_attempt_number=10)
    def new_or_get(self, client:Type[Client], prod_num:int, **kwargs):
        new_project, _ = self.get_or_create(
            client = client,
            production_number = prod_num,
            defaults = {'guid': generate(), **kwargs}
        )
        return new_project