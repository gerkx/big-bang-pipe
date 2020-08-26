from peewee import CharField, IntegrityError
from nanoid import generate

from .base_models import BaseModel


class Client(BaseModel):
    name = CharField(unique=True)

    def new(self, name):
        try:
            self.create(
                name = name,
                guid = generate()
            )
        except IntegrityError:
            
        # print(f"{new_client.name}, guid {new_client.guid} created" if created else print("already existed"))


    # def projects(self):
    #     return Client.get().projects

    