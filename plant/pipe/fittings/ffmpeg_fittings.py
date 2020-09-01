import os, subprocess
import os.path as path

from ...database.models import AudioGrab, Mix, Music, Stem
from .base_fittings import CPU_Fitting

class Transcode_To_MP3(CPU_Fitting):
    def fitting(self):
        if 'audio_db' in self.fso.props:
            audio_db = self.fso.props.audio_db
            if isinstance(audio_db, AudioGrab):
                subdir = 'Grab'
            if isinstance(audio_db, Mix):
                subdir = 'Mix'
            if isinstance(audio_db, Music):
                subdir = 'Music'
            if isinstance(audio_db, Stem):
                subdir = 'Stem'
        episode = str(self.fso.props.season * 100 + int(self.fso.props.episode)).zfill(3)
        transcode_dir = path.join(
            self.fso.props.editorial,
            'Referencias',
            'Audio',
            str(self.fso.props.season*100),
            episode,
            subdir
        )
        if not path.isdir(transcode_dir):
            os.makedirs(transcode_dir)
        transcode_path = path.join(transcode_dir, self.fso.name + '.mp3')
        ffmpeg_cmd = (
            f'ffmpeg -i {self.fso.path} -vn -ar 44100 -ac 2 -b:a 128k {transcode_path}'
        )
        subprocess.run(ffmpeg_cmd)
        self.fso.props.mp3_name = self.fso.name + '.mp3'
        self.fso.props.mp3_location = transcode_dir
