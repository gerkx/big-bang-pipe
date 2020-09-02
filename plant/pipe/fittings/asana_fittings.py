import json, os
from datetime import datetime, timedelta

from httpx import AsyncClient
from box import Box

from .base_fittings import Async_Fitting
from ...database.models import Project, Asana_Project, Asana_Tag, Asana_Task


def generate_due_tomorrow():
    tomorrow = datetime.now() + timedelta(1)
    return tomorrow.strftime('%Y-%m-%d')

def get_prod_num(props):
    if not 'episode' in props:
        epi = 99
    else:
        epi = props.episode
    return int(props.season) * 100 + int(epi)

def get_project(props):
    return Project().new_or_get(
            client = props.client,
            prod_num = get_prod_num(props))

async def get_asana_proj(client, props):
    try:
        proj = Asana_Project().get(Asana_Project.name == get_prod_num(props))
        print(f'found asana project in db: {proj.name}')
        return proj
    except:
        async with client as client:
            print('unable to find asana proj in db, posting to create new')
            header = {'Authorization': f'Bearer {os.getenv("ASANA_KEY")}'}
            data = {
                'name': get_prod_num(props),
                'team': os.getenv('ASANA_TEAM')
            }
            url = 'https://app.asana.com/api/1.0/projects'
            res = await client.post(url=url, data=data, headers=header)
            print(f"get asana proj res: ", res)
            res_data = Box(res.json()['data'])
            proj = Asana_Project().new_or_get(
                gid = res_data.gid,
                name = get_prod_num(props),
                project = props.project
            )
            return proj
            # try:
            # except:
            #     # TODO: Handle HTTP errors
            #     print('!!!! Need to handle http errors!!!!!!')


def construct_note(fso):
    if 'working_db' in fso.props:
        db = fso.props.working_db
    else:
        db = None
    print("db: "+ db.name)
    if db:
        if db.modified > db.created:
            return (
                f'{db.name} de episodio ' 
                f'{fso.props.project.production_number} ha sido actualizado y está localizado en:\n'
                f'{db.location}'
            )
        else:
            return (
                f'{db.name} de episodio' 
                f'{fso.props.project.production_number} ha sido ingresado y está localizado en:\n'
                f'{db.location}'
            )
    else:
        return (
            f'{fso.filename} ha sido ingresado y está localizado en:\n'
            f'{fso.directory}'
        )


class Asana_Create_Task(Async_Fitting):
    async def fitting(self):
        if not 'asana_project' in self.fso.props:
            if not 'project' in self.fso.props:
                self.fso.props.project = get_project(self.fso.props)
            print('getting asana project')
            self.fso.props.asana_project = await get_asana_proj(self.client, self.fso.props)
        async with self.client as client:
            header = {'Authorization': f'Bearer {os.getenv("ASANA_KEY")}'}
            data = {
                'name': self.fso.filename,
                'due_on': generate_due_tomorrow(),
                'assignee': 'me',
                'projects': self.fso.props.asana_project.gid,
                'notes': construct_note(self.fso)
            }
            url = 'https://app.asana.com/api/1.0/tasks'
            # try:
            res = await client.post(url=url, data=data, headers=header)
            print(f"{self.fso.filename} create asana task res: ", res)
            res_data = Box(res.json()['data'])
            db_data = {
                'gid': res_data.gid,
                'name': res_data.name,
                'project': self.fso.props.asana_project,
                'pipe_project': self.fso.props.project,
                'notes': res_data.notes,
            }
            if 'assignee' in res_data:
                db_data['assignee'] = res_data.assignee.gid
            self.fso.props.asana_task = Asana_Task().new_or_get(**db_data)
            # except:
            #     # TODO: Handle HTTP errors
            #     print('!!!! Need to handle http errors!!!!!!') 

