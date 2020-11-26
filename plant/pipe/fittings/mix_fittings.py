import os, shutil
from datetime import datetime
import os.path as path
from typing import Type

from .base_fittings import IO_Fitting
from ...database.models import (
    Client, Project, Music, Mix, Stem, WorkingAudio
)

class Set_Mix_Lang(IO_Fitting):
    def fitting(self):
        inbound_lang = self.fso.props.lang.lower()
        if inbound_lang is ('vo' or 'eng'):
            self.fso.props.lang = 'ENG'
        if inbound_lang is ('ve' or 'esp' or 'cast'):
            self.fso.props.lang = 'ESP'

class Set_Prod_Number(IO_Fitting):
    def fitting(self):
        self.fso.props.prod_number = (
            int(self.fso.props.season) * 100 + int(self.fso.props.episode)
        )

class Move_Mix_To_Server(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        server_dir = path.join(
            props.server,
            props.program,
            str(int(props.season)*100),
            self.fso.props.prod_number,
            'Audio',
            'Mix'
        )
        if not path.isdir(server_dir):
            os.makedirs(server_dir)
        server_path = path.join(server_dir, self.fso.filename)
        shutil.move(self.fso.path, server_path)
        self.fso.path = server_path

class Save_Mix_To_DB(IO_Fitting):
    def fitting(self):
        if not 'project' in self.fso.props:
            self.fso.props.project = Project().new_or_get(
                client = self.fso.props.client,
                prod_num = self.fso.props.prod_number
            )
        self.fso.props.audio_db = Mix().new_or_get(
            project = self.fso.props.project,
            inbound_name = self.fso.inbound_name,
            location = self.fso.directory,
            name = self.fso.filename
        )

class Copy_Mix_To_Edit(IO_Fitting):
    def fitting(self):
        edit_dir = path.join(
            self.fso.props.editorial,
            'Recursos',
            'Audio',
            str(int(self.fso.props.season)*100),
            self.fso.props.prod_number,
            'Mix'
        )
        if not path.isdir(edit_dir):
            os.makedirs(edit_dir)
        
        edit_filename = (
            f'monster_{self.fso.props.prod_number}_MIX_'
            f'{self.fso.props.lang}{self.fso.extension}'
        )
        edit_path = path.join(edit_dir, edit_filename)
        shutil.copy2(self.fso.path, edit_path)

# Add_Audio_To_WorkingAudio_DB
# Transcode_To_MP3
# Add_MP3_To_DB