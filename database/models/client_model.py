from peewee import CharField, IntegrityError
from nanoid import generate

from .base_models import BaseModel


class Client(BaseModel):
    name = CharField(unique=True)

    def new_or_get(self, name:str):
        new_client, _ = self.get_or_create(
            name = name,
            defaults = {
                'guid': generate()
            }
        )
        return new_client
    