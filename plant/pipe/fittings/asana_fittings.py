import asyncio, json, os
from datetime import datetime, timedelta

from httpx import AsyncClient, HTTPStatusError
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
        print(f'retrieved asana project {proj.name} from DB')
        return proj
    except:
        async with client as client:
            header = {'Authorization': f'Bearer {os.getenv("ASANA_KEY")}'}
            data = {
                'name': get_prod_num(props),
                'team': os.getenv('ASANA_TEAM')
            }
            url = 'https://app.asana.com/api/1.0/projects'
            print(data)
            try:
                print(f"posting new asana project for episode {get_prod_num(props)}")
                res = await client.post(url=url, data=data, headers=header)

                res_data = Box(res.json()['data'])
                proj = Asana_Project().new_or_get(
                    gid = res_data.gid,
                    name = get_prod_num(props),
                    project = props.project
                )
                return proj
            except HTTPStatusError as exc:
                print(f'Error response {exc.response.status_code} while posting proj for {get_prod_num(props)}')
                return None


def construct_note(fso):
    if str(fso.state) == 'ERROR':
        return f'{fso.filename} fue rechazado. Se puede localizarlo en {fso.path} '
    if 'working_db' in fso.props:
        db = fso.props.working_db
    else:
        db = None
    if db:
        shot = fso.props.shot_db
        project = fso.props.project
        if 'grade_db' in fso.props:
            if db.compo:
                return (
                    f'Plano {shot.shot} del episodio {project.production_number} '
                    f'tiene una nueva versión etalonada '
                    f'que se necesita integrar en el compo. '
                    f'El source del Compo está actualizado en {fso.props.compo_src_path}'
                )
            else:
                return (
                    f'Plano {shot.shot} del episodio {project.production_number} '
                    f'ha sido actualizado con una nueva versión etalonada. '
                    f'Está localizado en {db.location}'
                )


        elif 'render_db' in fso.props and (db.compo or db.grade):
            if db.grade:
                return (
                    f'Hay un nuevo render de shot {fso.props.shot_name} '
                    f'que necesita ser etalonado. El archivo está localizado en:\n'
                    f'{fso.path}'
                )
            else:
                return (
                    f'Plano {shot.shot} del episodio {project.production_number} '
                    f'tiene una nueva versión del render '
                    f'que se necesita integrar en el compo. '
                    f'El source del Compo está actualizado en {fso.props.compo_src_path}'
                )

        
        elif db.modified > db.created:
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
            self.fso.props.asana_project = await get_asana_proj(self.client, self.fso.props)
        
        if not self.fso.props.asana_project:
            return
        
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
            
            for _ in range(60):
                try:
                    print(f'posting new task for {self.fso.filename}')
                    res = await client.post(url=url, data=data, headers=header)
                    res.raise_for_status()
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
                
                except HTTPStatusError as exc:
                    print(f'Error response {exc.response.status_code} while posting task for {self.fso.filename}')
                    await asyncio.sleep(1)

                else:
                    break

        