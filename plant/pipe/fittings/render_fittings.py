import os, shutil
from datetime import datetime
import os.path as path
from typing import Type
from pathlib import Path

import fileseq

from .base_fittings import IO_Fitting

from ...database.models import (
    Client, Project, Shot, Render, Compo, Grade, WorkingPost
)


class Extract_All_Dirs(IO_Fitting):
    def fitting(self):
        self.fso.props.dirs = []
        root_path  = Path(self.fso.path)
        for p in root_path.rglob('**/'):
            if p.is_dir():
                self.fso.props.dirs.append(p)


class Detect_IMG_Sequences(IO_Fitting):
    def fitting(self):
        img_seqs = []
        for d in self.fso.props.dirs:
            p = d.__str__()
            dir_seq = fileseq.findSequenceOnDisk(p)
            img_seqs = [*img_seqs, *dir_seq]
        self.fso.props.img_seqs = img_seqs
        

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
class Rename_Dir_With_Vers(IO_Fitting):
    def fitting(self):
        if 'version' in self.fso.props:
            new_name = (
                f'{self.fso.props.shot_name}'
                f'_v{str(self.fso.props.version).zfill(3)}'
                f'{self.fso.extension}'
            )
            new_path = path.join(self.fso.directory, new_name)
            os.rename(self.fso.path, new_path)
            self.fso.path = new_path

# need to know how structure will be delivered to choose proper seq!!!!!!
class Rename_Seq_With_Vers(IO_Fitting):
    def fitting(self):
        # currently using first sequence found in directory
        seq = self.fso.props.img_seqs[0]
        seq_dir = seq.dirname()
        seq_basename = seq.basename().split(".")[0]
        vers_basename = (
            f'{seq_basename}_v{str(self.fso.props.version).zfill(3)}'
        )
        for idx, frame in enumerate(seq.frameSet()):
            frame_path = seq[idx]
            frame_num = str(frame).zfill(4)
            frame_vers_basename = (
                f'{vers_basename}.{frame_num}'
                f'{self.fso.etension}'
            )
            frame_vers_path = path.join(seq_dir, frame_vers_basename)

            os.rename(frame_path, frame_vers_path)

        self.fso.props.img_seqs[0].setBasename(f'{vers_basename}.')


class Move_Render_To_Server(IO_Fitting):
    def fitting(self):
        props = self.fso.props
        episode = str(int(props.season) * 100 + int(props.episode)).zfill(3)
        server_dir = path.join(
            props.server,
            props.program,
            str(int(props.season)*100),
            episode,
            'Video',
            'Render'
        )
        if not path.isdir(server_dir):
            os.makedirs(server_dir)
        server_path = path.join(server_dir, self.fso.filename)
        shutil.move(self.fso.path, server_path)
        self.fso.path = server_path


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

class Establish_Working_Dir(IO_Fitting):
    def fitting(self):
        working_db = self.fso.props.working_db
        if (working_db.compo or working_db.grade):
            if working_db.compo and not working_db.grade:
                if not path.isdir(self.fso.props.compo_src_dir):
                    os.makedirs(self.fso.props.compo_src_dir)
                self.fso.props.qt_dir = self.fso.props.compo_src_dir
        else:
            self.fso.props.qt_dir = self.fso.props.edit_shot_dir

# whuh? need to make a transcode path prop
# class Update_Edit_Shot(IO_Fitting):
#     def fitting(self):
#         working_db = self.fso.props.working_db
#         if (working_db.compo or working_db.grade):
#             if working_db.compo and not working_db.grade:
#                 if not path.isdir(self.fso.props.compo_src_dir):
#                      os.makedirs(self.fso.props.compo_src_dir)
#                 shutil.copy2(self.fso.path, self.fso.props.compo_src_path)
#         else:
#             shutil.copy2(self.fso.path, self.fso.props.edit_shot_path)
