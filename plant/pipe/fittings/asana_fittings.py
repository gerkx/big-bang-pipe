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
    return int(props.season) * 100 + int(props.episosode)

def get_project(props):
    print("getting Project()")
    return Project().new_or_get(
            client = props.client,
            prod_num = get_prod_num(props))

async def get_asana_proj(client, props):
    print("get_asana_proj")
    try:
        print("trying to get ASANA_PROJECT")
        proj = Asana_Project().get(Asana_Project.name == get_prod_num(props))
    except:
        print("except!")
        async with client as client:
            header = {'Authorization': f'Bearer {os.getenv("ASANA_KEY")}'}
            data = {
                'name': get_prod_num(props),
                'team': os.getenv('ASANA_TEAM')
            }
            url = 'https://app.asana.com/api/1.0/projects'
            try:
                res = await client.post(url=url, data=data, header=header)
                res_data = Box(json.loads(res.json())['data'])
                proj = Asana_Project().new_or_get(
                    gid = res_data.gid,
                    name = get_prod_num(props),
                    project = props.project
                )
            except:
                # TODO: Handle HTTP errors
                print('!!!! Need to handle http errors!!!!!!')

    return proj

def construct_note(fso):
    if 'working_audio_db' in fso.props:
        db = fso.props.working_audio_db
    elif 'working_vis_db' in fso.props:
        db = fso.props.working_vis_db
    else:
        db = None
        
    if db and db.modified > db.created:
        return (
            f'{db.name} de {db.project.name} ha sido actualizado y está localizado en:\n'
            f'{db.location}'
        )
    elif db:
        return (
            f'{db.name} de {db.project.name} ha sido ingresado y está localizado en:\n'
            f'{db.location}'
        )
    else:
        return (
            f'{fso.filename} ha sido ingresado y está localizado en:\n'
            f'{fso.directory}'
        )


class Asana_Create_Task(Async_Fitting):
    async def fitting(self):
        print("create_task: start")
        if not 'asana_project' in self.fso.props:
            print("create_task: no asana_project in props")
            if not 'project' in self.fso.props:
                print("create_task: no project in props")
                self.fso.props.project = get_project(self.fso.props)
            self.fso.props.asana_project = await get_asana_proj(self.client, self.fso.props)
        async with self.client as client:
            header = {'Authorization': f'Bearer {os.getenv("ASANA_KEY")}'}
            data = {
                'name': self.fso.filename,
                'due_on': generate_due_tomorrow(),
                'assignee': 'me',
                'projects': self.fso.props.asana_project,
                'notes': construct_note(self.fso)
            }
            url = 'https://app.asana.com/api/1.0/tasks'
            try:
                res = await client.post(url=url, data=data, header=header)
                res_data = Box(json.loads(res.json())['data'])
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
            except:
                # TODO: Handle HTTP errors
                print('!!!! Need to handle http errors!!!!!!') 

