import os, shutil
from datetime import datetime
import os.path as path
from typing import Type

from .base_fittings import IO_Fitting

from ...database.models import (
    Client, Project, Shot, Grade, WorkingPost
)

class Move_Grade_To_Server(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        episode = str(int(props.season) * 100 + int(props.episode)).zfill(3)
        server_dir = path.join(
            props.server,
            props.program,
            str(int(props.season)*100),
            episode,
            'Video',
            'Grade'
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


class Save_Grade_To_DB(IO_Fitting):
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
        
        self.fso.props.grade_db = Grade().new_or_get(
            shot = self.fso.props.shot_db,
            location = self.fso.directory,
            name = self.fso.name,
            inbound_name = self.fso.filename
        )

class Generate_Edit_Dirs(IO_Fitting):
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
        compo_src_dir = path.join(recursos_dir, 'Compo_Src')

        shot_dir = path.join(recursos_dir, 'Shots')
        if not path.isdir(shot_dir):
            os.makedirs(shot_dir)

        self.fso.props.compo_src_dir = compo_src_dir
        self.fso.props.edit_shot_dir = shot_dir

        edit_filename = f'{self.fso.props.shot_name}{self.fso.extension}'
        self.fso.props.edit_filename = edit_filename

        self.fso.props.compo_src_path = path.join(compo_src_dir, edit_filename)
        self.fso.props.edit_shot_path = path.join(shot_dir, edit_filename)


class Get_WorkingDB_Shot(IO_Fitting):
    def fitting(self):
        self.fso.props.working_db = WorkingPost().new_or_get(
            shot = self.fso.props.shot_db,
            name = self.fso.props.edit_filename,
            location = self.fso.props.edit_shot_path,
            grade = self.fso.props.grade_db
        )

class Update_Edit_Shot(IO_Fitting):
    def fitting(self):
        if not self.fso.props.working_db.compo:
            shutil.copy2(self.fso.path, self.fso.props.edit_shot_path)
        else: 
            if not path.isdir(self.fso.props.compo_src_dir):
                os.makedirs(self.fso.props.compo_src_dir)
            shutil.copy2(self.fso.path, self.fso.props.compo_src_path)

