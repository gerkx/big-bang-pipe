import os, shutil
from datetime import datetime
import os.path as path
from typing import Type

import fileseq

from .base_fittings import IO_Fitting

from ...database.models import (
    Client, Project, Shot, Render, Compo, Grade, WorkingPost
)

# class Detect_Img_Sequence(IO_Fitting):
#     def fitting(self):
        
        

class Generate_Shot_Name(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        self.fso.props.shot_name = (
            f'monster_S{str(int(props.season)).zfill(2)}'
            f'E{str(int(props.episode)).zfill(2)}_'
            f'SQ{str(int(props.sequence)).zfill(4)}_'
            f'SH{str(int(props.shot)).zfill(4)}'
        )

class Get_Project_DB(IO_Fitting):
    def fitting(self):
        client = self.fso.props.client
        prod_num = int(self.fso.props.season) * 100 + int(self.fso.props.episode)
        if not 'project' in self.fso.props:
            self.fso.props.project = Project().new_or_get(
                client = client,
                prod_num = prod_num
            )

class Get_Shot_DB(IO_Fitting):
    def fitting(self):
        if not 'shot_db' in self.fso.props:
            self.fso.props.shot_db = Shot().new_or_get(
                project = self.fso.props.project,
                name = self.fso.props.shot_name,
                shot = int(self.fso.props.shot)
            )

class Get_Version_Number(IO_Fitting):
    def fitting(self):
        prev_renders = self.fso.props.shot_db.renders
        self.fso.props.version = len(prev_renders) + 1

# need to know how structure of exrs will be before implementing namechanges, etc.

class Save_Render_To_DB(IO_Fitting):
    def fitting(self):
        self.fso.props.render_db = Compo().new_or_get(
            shot = self.fso.props.shot_db,
            location = self.fso.directory,
            name = self.fso.name,
            inbound_name = self.fso.filename,
        )

class Generate_Edit_Dirs(IO_Fitting):
    def fitting(self):
        recursos_dir = path.join(
            self.fso.props.editorial,
            'Recursos',
            'Video',
            str(int(self.fso.props.season)*100),
            self.fso.props.prod_number
        )

        self.fso.props.edit_shot_dir = path.join(recursos_dir, 'Shots')
        if not path.isdir(self.fso.props.edit_shot_dir):
            os.makedirs(self.fso.props.edit_shot_dir)

        self.fso.props.edit_filename = f'{self.fso.props.shot_name}{self.fso.extension}'
    
        self.fso.props.compo_src_dir = path.join(recursos_dir, 'Compo_Src')
        self.fso.props.compo_src_path = path.join(
            self.fso.props.compo_src_dir,
            self.fso.props.edit_filename)

        self.fso.props.edit_shot_path = path.join(
            self.fso.props.edit_shot_dir,
            self.fso.props.edit_filename
        )

class Get_WorkingDB_Shot(IO_Fitting):
    def fitting(self):
        self.fso.props.working_db = WorkingPost().new_or_get(
            shot = self.fso.props.shot_db,
            name = self.fso.props.edit_filename,
            location = self.fso.props.edit_shot_path,
            render = self.fso.props.render_db
        )

class Update_Edit_Shot(IO_Fitting):
    def fitting(self):
        working_db = self.fso.props.working_db
        if (working_db.compo or working_db.grade):
            if working_db.compo and not working_db.grade:
                if not path.isdir(self.fso.props.compo_src_dir):
                     os.makedirs(self.fso.props.compo_src_dir)
                shutil.copy2(self.fso.path, self.fso.props.compo_src_path)
        else:
            shutil.copy2(self.fso.path, self.fso.props.edit_shot_path)
