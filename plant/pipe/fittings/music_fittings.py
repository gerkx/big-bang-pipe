import os, shutil
from datetime import datetime
import os.path as path
from typing import Type

from .base_fittings import IO_Fitting
from ...database.models import (
    Client, Project, Music, Mix, Stem, WorkingAudio
)

class Move_Music_To_Server(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        episode = str(props.season * 100 + int(props.episode)).zfill(3)
        server_dir = path.join(
            props.server,
            props.program,
            str(int(props.season)*100),
            episode,
            'Audio',
            'Music'
        )
        if not path.isdir(server_dir):
            os.makedirs(server_dir)
        server_path = path.join(server_dir, self.fso.filename)
        shutil.move(self.fso.path, server_path)
        self.fso.path = server_path

class Save_Music_To_DB(IO_Fitting):
    def fitting(self):
        prod_num = int(self.fso.props.season) * 100 + int(self.fso.props.episode)
        if not 'project' in self.fso.props:
            self.fso.props.project = Project().new_or_get(
                client = self.fso.props.client,
                prod_num = prod_num
            )
        self.fso.props.audio_db = Music().new_or_get(
            project = self.fso.props.project,
            inbound_name = self.fso.inbound_name,
            location = self.fso.directory,
            name = self.fso.filename
        )

class Copy_Music_To_Edit(IO_Fitting):
    def fitting(self):
        episode = str(
            int(self.fso.props.season) * 100 + int(self.fso.props.episode)
        ).zfill(3)

        music_dir = path.join(
            self.fso.props.editorial,
            'Recursos',
            'Audio',
            str(int(self.fso.props.season)*100),
            episode,
            'Music'
        )
        if not path.isdir(music_dir):
            os.makedirs(music_dir)

        edit_filename = (
            f'monster_{episode}_MUSIC{self.fso.extension}'
        )
        music_path = path.join(music_dir, edit_filename)
        shutil.copy2(self.fso.path, music_path)
        self.fso.props.working_path = music_path



# Add_Audio_To_WorkingAudio_DB
# Transcode_To_MP3
# Add_MP3_To_DB