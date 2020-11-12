import os, shutil
from datetime import datetime
import os.path as path
from typing import Type

from .base_fittings import IO_Fitting

from ...database.models import (
    Client, Project, Shot, Motion, WorkingPost
)

class Move_Motion_To_Server(IO_Fitting):
    def fitting(self):
        props = self.fso.props

        episode = str(int(props.season) * 100 + int(props.episode)).zfill(3)
        server_dir = path.join(
            props.server,
            props.program,
            str(int(props.season)*100),
            episode,
            'Video',
            'Motion'
        )
        if not path.isdir(server_dir):
            os.makedirs(server_dir)
        server_path = path.join(server_dir, self.fso.filename)
        shutil.move(self.fso.path, server_path)
        self.fso.path = server_path

class Save_Motion_To_DB(IO_Fitting):
    def fitting(self):
        client = self.fso.props.client

        prod_number = (
            int(self.fso.props.season) * 100 + int(self.fso.props.episode)
        )
        if not 'project' in self.fso.props:
            self.fso.props.project = Project().new_or_get(
                client = client,
                prod_num = prod_number
            )
        if not 'shot_db' in self.fso.props:
            self.fso.props.shot_db = Shot().new_or_get(
                project = self.fso.props.project,
                name = self.fso.name,
                shot = int(self.fso.props.shot)+9000
            ) 

        self.fso.props.motion_db = Motion().new_or_get(
            shot = self.fso.props.shot_db,
            location = self.fso.directory,
            name = self.fso.name,
            inbound_name = self.fso.filename
        )

class Copy_Motion_To_Edit(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        episode = str(int(props.season) * 100 + int(props.episode)).zfill(3)
        motion_dir = path.join(
            props.editorial,
            'Recursos',
            'Video',
            str(int(props.season)*100),
            episode,
            'Motion'
        )
        if not path.isdir(motion_dir):
            os.makedirs(motion_dir)
        self.fso.props.edit_motion_dir = motion_dir

        edit_filename = (
            f'monster_{episode}_Motion_SH{str(int(self.fso.props.shot)+9000).zfill(4)}'
            f'{self.fso.extension}'
        )
        self.fso.props.edit_filename = edit_filename
        motion_path = path.join(motion_dir, edit_filename)

        shutil.copy2(self.fso.path, motion_path)

class Add_Motion_To_WorkingPost_DB(IO_Fitting):
    def fitting(self):
        self.fso.props.working_db = WorkingPost().new_or_get(
            shot = self.fso.props.shot_db,
            name = self.fso.props.edit_filename,
            location =  self.fso.props.edit_motion_dir,
            motion = self.fso.props.motion_db,
        )

class Add_MP4_To_DB(IO_Fitting):
    def fitting(self):
        if 'motion_db' in self.fso.props:
            self.fso.props.motion_db.mp4_name = self.fso.props.transcode_name
            self.fso.props.motion_db.mp4_location = self.fso.props.transcode_location
            self.fso.props.motion_db.save()
        else:
            print("!!!!! No Vis DB to add to !!!!")