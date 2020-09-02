import os, shutil
from datetime import datetime
import os.path as path
from typing import Type

# from box import Box
from .base_fittings import IO_Fitting
from ...database.models import Client, Project, AudioGrab, Music, Mix, Stem, WorkingAudio


class Rename_Audio_Grab(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        episode = str(props.season * 100 + int(props.episode)).zfill(3)
        take = 'retake' if 'retakes' in props.take.lower() else 'takes'
        char = props.char.lower().replace(' ', '')
        now = datetime.now()
        date =  str(now.year).zfill(2) + str(now.month).zfill(2) + str(now.day).zfill(2)

        new_name = f'{props.program}_{episode}_{take}_{char}_{date}{self.fso.extension}'
        new_path = path.join(self.fso.directory, new_name)

        os.rename(self.fso.path, new_path)
        self.fso.path = new_path


class Move_Audio_Grab_To_Server(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        episode = str(props.season * 100 + int(props.episode)).zfill(3)
        server_dir = path.join(
            props.server,
            props.program,
            str(props.season*100),
            episode,
            'Audio',
            'Grab'
        )
        if not path.isdir(server_dir):
            os.makedirs(server_dir)
        server_path = path.join(server_dir, self.fso.filename)
        shutil.move(self.fso.path, server_path)
        self.fso.path = server_path


class Save_Audio_Grab_To_DB(IO_Fitting):
    def fitting(self):
        client = self.fso.props.client

        prod_number = int(self.fso.props.season) * 100 + int(self.fso.props.episode)
        if not 'project' in self.fso.props:
            self.fso.props.project = Project().new_or_get(
                client = client,
                prod_num = prod_number,
            )
        self.fso.props.audio_db = AudioGrab().new_or_get(
            project = self.fso.props.project,
            inbound_name = self.fso.inbound_name,
            location = self.fso.directory,
            name = self.fso.filename,
            lang = self.fso.props.lang if 'lang' in self.fso.props else 'ENG'
        )


class Copy_Audio_Grab_To_Edit(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        episode = str(props.season * 100 + int(props.episode)).zfill(3)
        grab_dir = path.join(
            props.editorial, 
            'Recursos', 
            'Audio', 
            str(props.season*100),
            episode,
            'Grab')
        if not path.isdir(grab_dir):
            os.makedirs(grab_dir)
        grab_path = path.join(grab_dir, self.fso.filename)
        
        shutil.copy2(self.fso.path, grab_path)
        self.fso.props.working_path = grab_path


class Add_Audio_To_WorkingAudio_DB(IO_Fitting):
    def fitting(self):
        data = {
            'name': path.basename(self.fso.props.working_path),
            'location': path.dirname(self.fso.props.working_path),
            'project': self.fso.props.project,
        }
        if 'audio_db' in self.fso.props:
            audio_db = self.fso.props.audio_db
            if isinstance(audio_db, AudioGrab):
                data['grab'] = audio_db
            if isinstance(audio_db, Music):
                data['music'] = audio_db
            if isinstance(audio_db, Mix):
                data['mix'] = audio_db
            if isinstance(audio_db, Stem):
                data['stem'] = audio_db
        self.fso.props.working_audio_db = WorkingAudio().new_or_get(**data)
        print("added to workingaudio db")


class Add_MP3_To_DB(IO_Fitting):
    def fitting(self):
        if 'audio_db' in self.fso.props:
            self.fso.props.audio_db.mp3_name = self.fso.props.mp3_name
            self.fso.props.audio_db.mp3_location = self.fso.props.mp3_location
            self.fso.props.audio_db.save()
        else:
            print("!!!!! No Audio DB to add to !!!!")
        

        

        






