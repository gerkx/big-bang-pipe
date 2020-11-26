# from plant.pipe.fso.fso import create_FSO
from plant.pipe import Pipe
from plant.pipe.pipe_utils import init_Pipe
# from plant.pipe.pipe import Pipe
# from plant.queues.fifo_queue import FIFO_Queue
from plant.queues import Queue
from plant.pipe.filters.filter import Filter


from plant import Plant

import time
from box import Box

import httpx
import json
import asyncio

import fileseq

import os
import os.path as path
if __name__ == "__main__":

    # from peewee import *
    from datetime import date
    from nanoid import generate

    from peewee import OperationalError

    from plant.database.models import (
        Client, Project, Shot, AudioGrab, Music, Mix, Stem, WorkingAudio, 
        Asana_Project, Asana_Tag, Asana_Task, Asana_User, WorkingPost, Motion, Compo, Grade
    )


    seq_path = "Z:\\test\\seq"

    from pathlib import Path

    dirs = []
    
    pt = Path(seq_path)

    for p in pt.rglob("**/"):
        if p.is_dir():
            # print(p)
            dirs.append(p)


    print(dirs)

    # print(fileseq.findSequencesOnDisk(dirs[3].__str__()))
    seqs = []
    for d in dirs:
        p = d.__str__()
        seq_arr = fileseq.findSequencesOnDisk(p)
        seqs = [*seqs, *seq_arr]

    print(seqs)

    # try:
    #     print('zoinks')
    #     Client.create_table()
    # except OperationalError:
    #     print('Client table already exists')
    # try:
    #     Project.create_table()
    # except OperationalError:
    #     print('Project table already exists')
    # try:
    #     Shot.create_table()
    # except OperationalError:
    #     print('Shot table already exists')
    # try:
    #     AudioGrab.create_table()
    # except OperationalError:
    #     print('AudioGrab table already exists')
    # try:
    #     Music.create_table()
    # except OperationalError:
    #     print('Music table already exists')
    # try:
    #     Mix.create_table()
    # except OperationalError:
    #     print('Mix table already exists')
    # try:
    #     Stem.create_table()
    # except OperationalError:
    #     print('Stem table already exists')
    # try:
    #     WorkingAudio.create_table()
    # except OperationalError:
    #     print('WorkingAudio table already exists')
    # try:
    #     Asana_User.create_table()
    # except OperationalError:
    #     print('Asana_User table already exists')
    # try:
    #     Asana_Task.create_table()
    # except OperationalError:
    #     print('Asana_Task table already exists')
    # try:
    #     Asana_Project.create_table()
    # except OperationalError:
    #     print('Asana_Project table already exists')
    # try:
    #     Asana_Tag.create_table()
    # except OperationalError:
    #     print('Asana_Tag table already exists')
    # try:
    #     Motion.create_table()
    # except OperationalError:
    #     print('Motion table already exists')
    # try:
    #     Compo.create_table()
    # except OperationalError:
    #     print('Compo table already exists')
    # try:
    #     Grade.create_table()
    # except OperationalError:
    #     print('Grade table already exists')
    # try:
    #     WorkingPost.create_table()
    # except OperationalError:
    #     print('WorkingPost table already exists')
