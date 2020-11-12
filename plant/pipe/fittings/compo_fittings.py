import os, shutil
from datetime import datetime
import os.path as path
from typing import Type

from .base_fittings import IO_Fitting

from ...database.models import (
    Client, Project, Shot, Compo, WorkingPost
)

class Move_Compo_To_Server(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        episode = str(int(props.season) * 100 + int(props.episode)).zfill(3)
        server_dir = path.join(
            props.server,
            props.program,
            str(int(props.season)*100),
            episode,
            'Video',
            'Compo'
        )
        if not path.isdir(server_dir):
            os.makedirs(server_dir)
        server_path = path.join(server_dir, self.fso.filename)
        shutil.move(self.fso.path, server_path)
        self.fso.path = server_path

class Generate_Shot_Name(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        self.fso.props.shot_name = (
            f'monster_S{str(int(props.season)).zfill(2)}'
            f'E{str(int(props.episode)).zfill(2)}_'
            f'SQ{str(int(props.sequence)).zfill(4)}_'
            f'SH{str(int(props.shot)).zfill(4)}'
        )

class Save_Compo_To_DB(IO_Fitting):
    def fitting(self):
        client = self.fso.props.client
        prod_num = int(self.fso.props.season) * 100 + int(self.fso.props.episode)

        if not 'project' in self.fso.props:
            self.fso.props.project = Project().new_or_get(
                client = client,
                prod_num = prod_num
            )
        if not 'shot_db' in self.fso.props:
            self.fso.props.shot_db = Shot().new_or_get(
                project = self.fso.props.project,
                name = self.fso.props.shot_name,
                shot = int(self.fso.props.shot)
            )
        
        self.fso.props.compo_db = Compo().new_or_get(
            shot = self.fso.props.shot_db,
            location = self.fso.directory,
            name = self.fso.name,
            inbound_name = self.fso.filename,
        )

class Copy_Compo_To_Edit(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        episode = str(int(props.season) * 100 + int(props.episode)).zfill(3)
        recursos_dir = path.join(
            props.editorial,
            'Recursos',
            'Video',
            str(int(props.season)*100),
            episode,
        )
        shot_dir = path.join(recursos_dir, 'Shots')
        if not path.isdir(shot_dir):
            os.makedirs(shot_dir)

        self.fso.props.edit_shot_dir = shot_dir
        shot_name = self.fso.props.shot_name
        edit_filename = f'{shot_name}{self.fso.extension}'
        self.fso.props.edit_filename = edit_filename

        self.fso.props.edit_shot_path = path.join(shot_dir, edit_filename)

        shutil.copy2(
            self.fso.path, 
            self.fso.props.edit_shot_path
        )

class Add_Compo_To_WorkingPost_DB(IO_Fitting):
    def fitting(self):
        self.fso.props.working_db = WorkingPost().new_or_get(
            shot = self.fso.props.shot_db,
            name = self.fso.props.edit_filename,
            location = self.fso.props.edit_shot_path,
            compo = self.fso.props.compo_db
        )




