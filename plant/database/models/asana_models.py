from typing import Type

from nanoid import generate
from peewee import (
    CharField, ForeignKeyField, TextField
)

from .base_models import BaseModel
from .user_model import User
from .project_model import Project


class Asana_User(BaseModel):
    user = ForeignKeyField(User, backref='asana_users', null=True)
    name = CharField()
    gid = CharField()
    email = CharField()

    def new_or_get(self,
        gid:str,
        name:str,
        email:str,
        **kwargs
    ):
        asana_user, _ = self.get_or_create(
            gid = gid,
            defaults = {
                'email': email,
                'guid': generate(),
                'name': name,
                **kwargs
            }
        )
        return asana_user

class Asana_Project(BaseModel):
    project = ForeignKeyField(Project, backref='asana_projects', null=True)
    gid = CharField()
    name = CharField(unique=True)

    def new_or_get(self,
        gid:str,
        name:str,
        **kwargs
    ):
        asana_project, _ = self.get_or_create(
            name = name,
            defaults = {
                'guid': generate(),
                 'gid': gid,
                **kwargs
            }
        )
        return asana_project

class Asana_Tag(BaseModel):
    gid = CharField()
    name = CharField(unique=True)

    def new_or_get(self,
        gid:str,
        name:str
    ):
        asana_tag, _ = self.get_or_create(
            gid = gid,
            defaults = {
               'guid': generate(),
               'name': name,
            }
        )
        return asana_tag

class Asana_Task(BaseModel):
    project = ForeignKeyField(Asana_Project, backref='tasks')
    pipe_project = ForeignKeyField(Project, backref='tasks', null=True)
    assignee = ForeignKeyField(Asana_User, backref='tasks', null=True)
    gid = CharField()
    name = CharField(null=True)
    notes = TextField(null=True)

    def new_or_get(self,
        project:Type[Asana_Project],
        gid:str,
        **kwargs
    ):
        asana_task, _ = self.get_or_create(
            gid = gid,
            defaults = {
                'project': project,
                'guid': generate(),
                **kwargs
            }
        )
        return asana_task

