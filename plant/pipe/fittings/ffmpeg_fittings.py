import os, subprocess
import os.path as path
import time

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
        episode = str(int(self.fso.props.season) * 100 + int(self.fso.props.episode)).zfill(3)
        transcode_dir = path.join(
            self.fso.props.editorial,
            'Referencias',
            'Audio',
            str(int(self.fso.props.season)*100),
            episode,
            subdir
        )
        if not path.isdir(transcode_dir):
            os.makedirs(transcode_dir)
        transcode_path = path.join(transcode_dir, self.fso.name + '.mp3')
        ffmpeg_cmd = (
            f'ffmpeg -i "{self.fso.path}" -vn -ar 44100 -ac 2 -b:a 128k -y "{transcode_path}"'
        )
        subprocess.run(ffmpeg_cmd)
        self.fso.props.mp3_name = self.fso.name + '.mp3'
        self.fso.props.mp3_location = transcode_dir

class Transcode_To_MP4(CPU_Fitting):
    def fitting(self):
        episode = str(int(self.fso.props.season) * 100 + int(self.fso.props.episode)).zfill(3)
        if 'motion_db' in self.fso.props:
            subdir = 'Motion'
        if 'compo_db' in self.fso.props:
            subdir = 'Compo'
        if 'grade_db' in self.fso.props:
            subdir = 'Grade'

        transcode_dir = path.join(
            self.fso.props.editorial,
            'Referencias',
            'Video',
            str(int(self.fso.props.season)*100),
            episode,
            subdir
        )
        if not path.isdir(transcode_dir):
            os.makedirs(transcode_dir)
        if ('edit_filename' in self.fso.props):
            trans_name = path.splitext(self.fso.props.edit_filename)[0]
        else:
            trans_name = self.fso.name
        transcode_path = path.join(transcode_dir, trans_name + '.mp4')
        ffmpeg_cmd = (
            f'ffmpeg -i "{self.fso.path}" -c:v libx264 -preset veryfast' 
            f' -pix_fmt yuv420p -y "{transcode_path}"'
        )
        subprocess.run(ffmpeg_cmd)
        self.fso.props.transcode_name = self.fso.name + '.mp4'
        self.fso.props.transcode_location = transcode_dir

class Transcode_To_MJPEG_QT(CPU_Fitting):
    def fitting(self):
        subdir_name = (
            f'Planos_S{str(int(self.fso.props.season)).zfill(2)}'
            f'E{str(int(self.fso.props.episode)).zfill(2)}'
        )
        subdir = path.join(self.fso.directory, subdir_name)
        if not path.isdir(subdir):
            os.makedirs(subdir)
        
        transcode_path = path.join(subdir, self.fso.name + '.mov')

        ffmpeg_cmd = (
            f'ffmpeg -i "{self.fso.path}" -timecode 00:00:00:00 -map 0:v:0 -map 0:a:0 '
            f'-pix_fmt yuvj422p -vcodec mjpeg -acodec copy -f mov -y "{transcode_path}"'
        )
        subprocess.run(ffmpeg_cmd)
        self.fso.props.shotgun_qt_path = transcode_path 

class Transcode_Char_Audio(CPU_Fitting):
    def fitting(self):
        shot_name = (
            f'monster_S{str(int(self.fso.props.season)).zfill(2)}'
            f'E{str(int(self.fso.props.episode)).zfill(2)}'
            f'_SQ{str(int(self.fso.props.sequence)).zfill(4)}'
            f'_SH{str(int(self.fso.props.shot)).zfill(4)}'
        )

        audio_dir = path.join(self.fso.directory, 'audio', shot_name)
        if not path.isdir(audio_dir):
            os.makedirs(audio_dir)
        chars = ['haha', 'hehe', 'hihi', 'hoho', 'huhu', 'ninos_y_grupo']
        char_audios = []
        for idx, char in enumerate(chars):
            char_path = path.join(audio_dir, f'{self.fso.name}_{char}.aif')
            ffmpeg_cmd = (
                f'ffmpeg -i "{self.fso.path}" -timecode 00:00:00:00 ' 
                f'-map 0:a:{idx + 1} -vn -acodec copy -f aiff -y ' 
                f'"{char_path}"'
            )
            subprocess.run(ffmpeg_cmd)
            char_audios.append(char_path)
        self.fso.props.shotgun_audio_dir = audio_dir
        self.fso.props.shotgun_audio_files = char_audios
        self.fso.props.shot_name = shot_name
        time.sleep(.1)

