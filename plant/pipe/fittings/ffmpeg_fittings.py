import subprocess
import os.path as path

from .base_fittings import CPU_Fitting

class Transcode_To_MP3(CPU_Fitting):
    def fitting(self):
        episode = str(self.fso.props.season * 100 + int(self.fso.props.episode)).zfill(3)
        transcode_dir = path.join(
            self.fso.props.editorial,
            'Referencias',
            'Audio',
            str(self.fso.props.season*100),
            episode,
            'Grab'
        )
        transcode_path = path.join(transcode_dir, self.fso.name + '.mp3')
        ffmpeg_cmd = (
            f'ffmpeg -i {self.fso.path} -vn -ar 44100 -ac 2 -b:a 128k {transcode_path}'
        )
        subprocess.run(ffmpeg_cmd)
        self.fso.props.mp3_name = self.fso.name + '.mp3'
        self.fso.props.mp3_location = transcode_dir
