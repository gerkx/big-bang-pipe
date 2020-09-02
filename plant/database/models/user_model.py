import bcrypt
from peewee import CharField
from nanoid import generate
from retrying import retry

from .base_models import BaseModel


class User(BaseModel):
    first_name:str = CharField()
    last_name:str = CharField()
    email:str = CharField(unique=True)
    password:str = CharField()
    phone:str = CharField(null=True)

    @staticmethod
    def hash_pass(raw_pass_str:str) -> str:
        encoded_pass = raw_pass_str.encode('utf-8')
        return bcrypt.hashpw(encoded_pass, bcrypt.gensalt())

    @retry(wait_random_min=250, wait_random_max=2000, stop_max_attempt_number=10)
    def new_or_get(self,
        first_name:str,
        last_name:str,
        email:str,
        password:str,
        **kwargs
    ):
        user, _ = self.get_or_create(
            email = email,
            defaults = {
                'guid': generate(),
                'first_name': first_name,
                'last_name': last_name,
                'password': self.hash_pass(password),
                **kwargs
            }
        )
        return user


