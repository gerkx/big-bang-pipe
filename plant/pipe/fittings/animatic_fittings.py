import os, shutil, stat, time
from datetime import datetime
import os.path as path
from typing import Type


from .base_fittings import IO_Fitting

from ...database.models import (
    Client, Project, Shot, WorkingPost,
)

class Move_Animatic_To_Exchange(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        sea = f'S{str(int(props.season)).zfill(2)}'
        epi = f'EP{str(int(props.episode)).zfill(2)}'
        animatic_dir = path.join(props.animatic_exchange, sea, epi)
        if not path.isdir(animatic_dir):
            os.makedirs(animatic_dir)
        animatic_path = path.join(animatic_dir, self.fso.filename)
        shutil.move(self.fso.path, animatic_path)
        self.fso.path = animatic_path
        
class Save_Shot_To_DB(IO_Fitting):
    def fitting(self):
        prod_number = (
            (int(self.fso.props.season) * 100) + int(self.fso.props.episode) 
        )

        if not 'project' in self.fso.props:
            self.fso.props.project = Project().new_or_get(
                client = self.fso.props.client,
                prod_num = prod_number
            )
        
        if not 'shot_db' in self.fso.props:
            self.fso.props.shot_db = Shot().new_or_get(
                project = self.fso.props.project,
                name = self.fso.name,
                shot = int(self.fso.props.shot)
            )

class Zip_Char_Audios(IO_Fitting):
    def remove_readonly(self, func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def fitting(self):
        # zip_dir = audio_dir = path.join(self.fso.directory, 'audio')
        if 'shotgun_audio_dir' in self.fso.props:
            audio_dir = self.fso.props.shotgun_audio_dir
            shutil.make_archive(
                audio_dir, 
                'zip', 
                audio_dir
            )
            time.sleep(.1)
            shutil.rmtree(audio_dir, onerror=self.remove_readonly)

class Copy_Shots_To_Edit(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        episode = str(int(props.season) * 100 + int(props.episode)).zfill(3)
        shot_dir = path.join(
            props.editorial,
            'Recursos',
            'Video',
            str(int(props.season)*100),
            episode,
            'Shots'
        )
        if not path.isdir(shot_dir):
            os.makedirs(shot_dir)

        self.fso.props.edit_shot_dir = shot_dir
        shot_path = path.join(shot_dir, f'{props.shot_name}{self.fso.extension}')
        self.fso.props.edit_shot_path = shot_path

        shutil.copy2(props.shotgun_qt_path, shot_path)

class Add_Shot_To_WorkingPost_DB(IO_Fitting):
    def fitting(self):
        self.fso.props.working_db = WorkingPost().new_or_get(
            shot = self.fso.props.shot_db,
            name = f'{self.fso.props.shot_name}{self.fso.extension}',
            location = self.fso.props.edit_shot_dir
        )



class Remove_Original_QT(IO_Fitting):
    def fitting(self):
        os.remove(self.fso.path)