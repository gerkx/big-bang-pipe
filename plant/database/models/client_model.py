from peewee import CharField, IntegrityError
from nanoid import generate
from retrying import retry

from .base_models import BaseModel


class Client(BaseModel):
    name = CharField(unique=True)

    @retry(wait_random_min=250, wait_random_max=2000, stop_max_attempt_number=10)
    def new_or_get(self, name:str):
        new_client, _ = self.get_or_create(
            name = name,
            defaults = {
                'guid': generate()
            }
        )
        return new_client
    